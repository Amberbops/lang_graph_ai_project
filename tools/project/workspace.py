from pathlib import Path
import shutil
import threading
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BASE_PROJECT_ROOT = REPO_ROOT / "generated_project"

# Thread-local storage for multi-user session isolation
_local_context = threading.local()


def set_current_user_context(user_id: Optional[str]):
    """Set the active user ID for the current generation thread."""
    _local_context.user_id = (user_id or "default").strip()


def get_current_user_context() -> str:
    """Retrieve the active user ID for the current thread."""
    return getattr(_local_context, "user_id", "default")


def get_user_workspace_root(user_id: Optional[str] = None) -> Path:
    """Returns the workspace root folder scoped to a specific user."""
    uid = user_id or get_current_user_context()
    if uid == "default":
        return BASE_PROJECT_ROOT
    return BASE_PROJECT_ROOT / "users" / uid


# Maintain backwards compatibility
PROJECT_ROOT = BASE_PROJECT_ROOT


def init_project_root(clean: bool = True, user_id: Optional[str] = None) -> Path:
    """Create and optionally reset the generated project workspace for a user."""
    root = get_user_workspace_root(user_id)
    if clean and root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    return root


def safe_path_for_project(path: str = "", user_id: Optional[str] = None) -> Path:
    """
    Resolve a Path safely inside the user's generated project workspace.
    Prevents path traversal outside the user's workspace.
    """
    root = get_user_workspace_root(user_id)
    root.mkdir(parents=True, exist_ok=True)

    if not path or path.strip() == "":
        return root

    resolved_root = root.resolve()
    candidate = (root / path).resolve()

    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError(
            f"Attempt to access outside project root.\n"
            f"root={resolved_root}\n"
            f"candidate={candidate}"
        )
    return candidate


def get_current_directory() -> Path:
    """Return the absolute user workspace path."""
    return str(get_user_workspace_root().resolve())