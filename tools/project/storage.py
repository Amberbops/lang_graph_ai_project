"""
Supabase Storage & Auth adapter for DevPilot.

Features:
- User-scoped bucket storage: devpilot-projects/users/{user_id}/...
- Clears user storage space to 0 on new generation requests
- Cloud-first streaming of ZIP and previews per user
- Supabase Auth helpers (signup, signin, verify)
"""

import os
import io
import zipfile
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BUCKET_NAME = "devpilot-projects"
_supabase_client = None


def get_supabase_client():
    """Initializes and returns the Supabase client if credentials are configured."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        return None

    try:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as exc:
        logger.warning(f"Could not initialize Supabase client: {exc}")
        return None


# -----------------------------------------------------------------------------
# User Storage Scope Helper
# -----------------------------------------------------------------------------

def _resolve_user_cloud_path(user_id: Optional[str], path: str) -> str:
    """Builds a partitioned cloud path for a specific user."""
    clean_p = path.replace("\\", "/").lstrip("/")
    uid = (user_id or "default").strip()
    return f"users/{uid}/{clean_p}"


def clear_user_cloud_storage(user_id: Optional[str]) -> bool:
    """
    Clears all files in the user's specific storage bucket partition to 0.
    Called before starting a new synthesis run.
    """
    client = get_supabase_client()
    if not client:
        return False

    uid = (user_id or "default").strip()
    folder_prefix = f"users/{uid}"

    try:
        files = client.storage.from_(BUCKET_NAME).list(folder_prefix)
        if not files:
            return True

        paths_to_delete = [
            f"{folder_prefix}/{f['name']}"
            for f in files
            if f.get("name") and not f.get("name").startswith(".")
        ]

        if paths_to_delete:
            client.storage.from_(BUCKET_NAME).remove(paths_to_delete)
            logger.info(f"Cleared {len(paths_to_delete)} files for user '{uid}' from cloud storage.")
        return True
    except Exception as exc:
        logger.warning(f"Error clearing cloud storage for user '{uid}': {exc}")
        return False


def upload_project_file(relative_path: str, content: str, user_id: Optional[str] = None) -> Optional[str]:
    """
    Upload or overwrite a file in Supabase Storage under users/{user_id}/...
    """
    client = get_supabase_client()
    if not client:
        return None

    target_path = _resolve_user_cloud_path(user_id, relative_path)

    # Detect MIME type
    clean_path = relative_path.replace("\\", "/").lstrip("/")
    ext = clean_path.rsplit(".", 1)[-1].lower() if "." in clean_path else ""
    content_types = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "txt": "text/plain",
        "md": "text/markdown",
        "svg": "image/svg+xml",
        "ico": "image/x-icon",
        "png": "image/png",
        "jpg": "image/jpeg",
    }
    content_type = content_types.get(ext, "text/plain")

    try:
        data_bytes = content.encode("utf-8")
        client.storage.from_(BUCKET_NAME).upload(
            path=target_path,
            file=data_bytes,
            file_options={"content-type": content_type, "upsert": "true"}
        )
        return target_path
    except Exception as exc:
        logger.warning(f"Failed to sync {target_path} to Supabase Storage: {exc}")
        return None


def list_cloud_files(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all generated project files stored for a specific user.
    """
    client = get_supabase_client()
    if not client:
        return []

    uid = (user_id or "default").strip()
    folder_prefix = f"users/{uid}"

    try:
        files = client.storage.from_(BUCKET_NAME).list(folder_prefix)
        return [f for f in files if f.get("name") and not f.get("name").startswith(".")]
    except Exception as exc:
        logger.warning(f"Failed to list files for user '{uid}': {exc}")
        return []


def download_cloud_file(file_path: str, user_id: Optional[str] = None) -> Optional[bytes]:
    """
    Download raw bytes of a file from Supabase Storage for a specific user.
    """
    client = get_supabase_client()
    if not client:
        return None

    target_path = _resolve_user_cloud_path(user_id, file_path)
    try:
        return client.storage.from_(BUCKET_NAME).download(target_path)
    except Exception as exc:
        logger.warning(f"Failed to download {target_path} from Supabase: {exc}")
        return None


def build_cloud_zip_buffer(user_id: Optional[str] = None) -> Optional[bytes]:
    """
    Fetches all files directly from Supabase Storage for a specific user
    and compiles an in-memory ZIP archive bytes.
    """
    client = get_supabase_client()
    if not client:
        return None

    files = list_cloud_files(user_id=user_id)
    if not files:
        return None

    zip_buffer = io.BytesIO()
    file_count = 0

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_info in files:
            name = file_info.get("name")
            if not name:
                continue
            data = download_cloud_file(name, user_id=user_id)
            if data is not None:
                zf.writestr(name, data)
                file_count += 1

    if file_count == 0:
        return None

    return zip_buffer.getvalue()


# -----------------------------------------------------------------------------
# Supabase Authentication Helpers
# -----------------------------------------------------------------------------

def auth_sign_up(email: str, password: str) -> Dict[str, Any]:
    """Registers a new user in Supabase Auth."""
    client = get_supabase_client()
    if not client:
        return {"error": "Supabase client not configured"}
    try:
        res = client.auth.sign_up({"email": email, "password": password})
        if res.user:
            token = res.session.access_token if res.session else None
            return {
                "success": True,
                "user_id": res.user.id,
                "email": res.user.email,
                "access_token": token,
                "email_confirmed": bool(res.user.email_confirmed_at),
            }
        return {"error": "User creation failed"}
    except Exception as exc:
        return {"error": str(exc)}


def auth_sign_in(email: str, password: str) -> Dict[str, Any]:
    """Signs in an existing user with Supabase Auth."""
    client = get_supabase_client()
    if not client:
        return {"error": "Supabase client not configured"}
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        if res.user and res.session:
            return {
                "success": True,
                "user_id": res.user.id,
                "email": res.user.email,
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
            }
        return {"error": "Invalid email or password"}
    except Exception as exc:
        return {"error": str(exc)}


def auth_get_user(access_token: str) -> Optional[Dict[str, Any]]:
    """Validates an access token and returns user details."""
    client = get_supabase_client()
    if not client or not access_token:
        return None
    try:
        user = client.auth.get_user(access_token)
        if user and user.user:
            return {
                "user_id": user.user.id,
                "email": user.user.email,
            }
        return None
    except Exception:
        return None
