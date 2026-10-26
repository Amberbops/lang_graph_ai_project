"""
Neon Project Generator — Web Backend Server
Zero-dependency HTTP server built with Python standard library.
Provides live agent tracking, Antigravity-style elapsed timers, and ZIP export.
"""

import io
import json
import mimetypes
import os
import sys
import threading
import time
import zipfile
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Add project root to sys.path so agents_v2 and tools can be imported
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_DIR))

from tools.project.workspace import PROJECT_ROOT, init_project_root

# Static files directory
STATIC_DIR = Path(__file__).resolve().parent / "static"

# ==============================================================================
# Global Generation State
# ==============================================================================

pipeline_lock = threading.Lock()

generation_state = {
    "is_running": False,
    "prompt": "",
    "start_time": 0.0,
    "end_time": 0.0,
    "elapsed_seconds": 0.0,
    "current_step_id": "",
    "status": "IDLE",  # IDLE, RUNNING, COMPLETED, FAILED
    "error_message": "",
    "steps": [
        {"id": "router", "title": "Router", "icon": "🧭", "description": "Analyzing intent & classifying request", "status": "pending", "duration": 0.0, "start_time": 0.0},
        {"id": "inspector", "title": "Workspace Inspector", "icon": "🔍", "description": "Scanning project filesystem & dependencies", "status": "pending", "duration": 0.0, "start_time": 0.0},
        {"id": "architect", "title": "System Architect", "icon": "📐", "description": "Designing technical architecture & components", "status": "pending", "duration": 0.0, "start_time": 0.0},
        {"id": "planner", "title": "Strategic Planner", "icon": "📋", "description": "Breaking architecture into prioritized tasks", "status": "pending", "duration": 0.0, "start_time": 0.0},
        {"id": "coder", "title": "Coding Agent", "icon": "⚡", "description": "Writing code, styling & application files", "status": "pending", "duration": 0.0, "start_time": 0.0},
        {"id": "tester", "title": "Verification & Tester", "icon": "🧪", "description": "Executing test suites & validating output", "status": "pending", "duration": 0.0, "start_time": 0.0},
        {"id": "packager", "title": "ZIP Packager", "icon": "📦", "description": "Compressing project into downloadable ZIP archive", "status": "pending", "duration": 0.0, "start_time": 0.0},
    ],
    "logs": [],
    "files_generated": [],
    "test_summary": "",
    "zip_ready": False,
}


def log_event(message: str, level: str = "info"):
    """Append a timestamped log to the generation state."""
    timestamp = time.strftime("%H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "message": message,
        "level": level,
    }
    with pipeline_lock:
        generation_state["logs"].append(entry)
        if len(generation_state["logs"]) > 200:
            generation_state["logs"].pop(0)
    print(f"[{timestamp}] [{level.upper()}] {message}")


def update_step(step_id: str, status: str, duration: float = 0.0):
    """Update a pipeline step's status and timing."""
    with pipeline_lock:
        for s in generation_state["steps"]:
            if s["id"] == step_id:
                s["status"] = status
                if status == "running":
                    s["start_time"] = time.time()
                    generation_state["current_step_id"] = step_id
                elif status in ("completed", "failed"):
                    if s["start_time"] > 0:
                        s["duration"] = round(time.time() - s["start_time"], 2)
                    elif duration > 0:
                        s["duration"] = round(duration, 2)
                break


def reset_generation_state():
    """Reset the pipeline state for a new run."""
    with pipeline_lock:
        generation_state["is_running"] = False
        generation_state["prompt"] = ""
        generation_state["start_time"] = 0.0
        generation_state["end_time"] = 0.0
        generation_state["elapsed_seconds"] = 0.0
        generation_state["current_step_id"] = ""
        generation_state["status"] = "IDLE"
        generation_state["error_message"] = ""
        generation_state["logs"] = []
        generation_state["files_generated"] = []
        generation_state["test_summary"] = ""
        generation_state["zip_ready"] = False
        for s in generation_state["steps"]:
            s["status"] = "pending"
            s["duration"] = 0.0
            s["start_time"] = 0.0


# ==============================================================================
# Background Agent Pipeline Runner
# ==============================================================================

def run_agent_pipeline(prompt: str, clean_workspace: bool = True, user_id: str = "default"):
    """Execute DevPilot LangGraph chain with user-isolated cloud and local workspaces."""
    try:
        from agents_v2.graph import app
        from tools.project.workspace import (
            set_current_user_context,
            init_project_root,
            get_user_workspace_root,
        )
        from tools.project.storage import clear_user_cloud_storage, list_cloud_files

        # Set thread-local user context
        set_current_user_context(user_id)

        with pipeline_lock:
            generation_state["is_running"] = True
            generation_state["status"] = "RUNNING"
            generation_state["start_time"] = time.time()
            generation_state["prompt"] = prompt
            generation_state["user_id"] = user_id

        log_event(f"Starting pipeline for user [{user_id}] | Prompt: \"{prompt}\"")

        # REQUIREMENT: Each request of the individual clears its specific storage space in the bucket to 0!
        if clean_workspace:
            log_event(f"Clearing cloud bucket partition (users/{user_id}/) to 0...", "info")
            clear_user_cloud_storage(user_id)
            log_event("User cloud partition cleared to 0 bytes.", "info")
            init_project_root(clean=True, user_id=user_id)
        else:
            init_project_root(clean=False, user_id=user_id)

        initial_state = {
            "user_request": prompt,
            "messages": [],
            "errors": [],
            "files_changed": [],
            "tool_calls_count": 0,
            "iteration": 0,
            "debug_iteration": 0,
        }

        # Step 1: Router
        update_step("router", "running")
        log_event("Classifying prompt intent...")

        # Stream LangGraph events to update timers per node
        final_result = None
        current_node = "router"
        run_thread_id = f"devpilot_{user_id}_{int(time.time())}"

        stream_config = {
            "recursion_limit": 150,
            "configurable": {"thread_id": run_thread_id},
        }

        for chunk in app.stream(initial_state, stream_config):
            for node_name, state_update in chunk.items():
                log_event(f"Node finished turn: {node_name}", "info")

                # Advance to next logical step
                if node_name == "router":
                    update_step("router", "completed")
                    intent = state_update.get("intent", "CREATE")
                    log_event(f"Intent classified: {intent}")
                    update_step("inspector", "running")
                elif node_name == "inspector":
                    update_step("inspector", "completed")
                    update_step("architect", "running")
                elif node_name == "architect":
                    update_step("architect", "completed")
                    arch = state_update.get("architecture", {})
                    summary = arch.get("summary", "Architecture designed.")
                    log_event(f"Architecture ready: {summary[:100]}...")
                    update_step("planner", "running")
                elif node_name == "planner":
                    update_step("planner", "completed")
                    plan = state_update.get("plan", {})
                    goal = plan.get("goal", "Plan ready.")
                    log_event(f"Plan ready: {goal[:100]}...")
                    update_step("coder", "running")
                elif node_name == "coder":
                    files = state_update.get("files_changed", [])
                    status = state_update.get("status", "")
                    log_event(f"Coder turn: status={status}, files changed so far: {len(files)}")
                    if status in ("CODER_DONE", "CODER_LIMIT_REACHED"):
                        update_step("coder", "completed")
                        update_step("tester", "running")
                    else:
                        # Still executing tools — ensure coder stays running
                        update_step("coder", "running")
                elif node_name == "tester":
                    test_res = state_update.get("test_results", {})
                    succ = test_res.get("success", True)
                    summary = test_res.get("summary", "Tests executed.")
                    generation_state["test_summary"] = summary
                    log_event(f"Tester finished: {summary}")
                    update_step("tester", "completed")

                final_result = state_update

        # Make sure earlier steps are marked completed if skipped
        for s in ("router", "inspector", "architect", "planner", "coder", "tester"):
            update_step(s, "completed")

        # Step 7: Packaging ZIP
        update_step("packager", "running")
        log_event("Packaging files into ZIP archive...")
        time.sleep(0.4)

        # Inspect generated files for this specific user
        files_list = []
        user_root = get_user_workspace_root(user_id)
        if user_root.exists():
            for f in sorted(user_root.rglob("*")):
                if f.is_file():
                    rel = str(f.relative_to(user_root))
                    size = f.stat().st_size
                    files_list.append({"name": rel, "size": size})

        with pipeline_lock:
            generation_state["files_generated"] = files_list
            generation_state["zip_ready"] = True
            generation_state["end_time"] = time.time()
            generation_state["elapsed_seconds"] = round(generation_state["end_time"] - generation_state["start_time"], 2)
            generation_state["status"] = "COMPLETED"
            generation_state["is_running"] = False

        update_step("packager", "completed")
        log_event(f"Project generation complete! {len(files_list)} files generated in {generation_state['elapsed_seconds']}s.", "success")


    except Exception as exc:
        log_event(f"Pipeline error: {exc}", "error")
        with pipeline_lock:
            generation_state["is_running"] = False
            generation_state["status"] = "FAILED"
            generation_state["error_message"] = str(exc)
            generation_state["end_time"] = time.time()
            generation_state["elapsed_seconds"] = round(generation_state["end_time"] - generation_state["start_time"], 2)


# ==============================================================================
# HTTP Request Handler
# ==============================================================================

class NeonGeneratorHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler serving the Neon UI and REST APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        """Handle GET requests for static files and APIs."""
        path_only = self.path.split("?")[0]
        if path_only in ("/", "/login", "/login.html"):
            self.serve_file(STATIC_DIR / "login.html", "text/html")
        elif path_only in ("/app", "/app.html", "/index.html", "/console", "/workspace"):
            self.serve_file(STATIC_DIR / "index.html", "text/html")
        elif path_only in ("/about", "/about.html"):
            self.serve_file(STATIC_DIR / "about.html", "text/html")
        elif path_only == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        elif path_only in ("/health", "/api/health"):
            self.send_json({"status": "healthy", "service": "DevPilot Synthesis Gateway"})
        elif path_only == "/style.css":
            self.serve_file(STATIC_DIR / "style.css", "text/css")
        elif path_only == "/app.js":
            self.serve_file(STATIC_DIR / "app.js", "application/javascript")
        elif self.path.startswith("/api/auth/me"):
            self.handle_auth_me()
        elif self.path.startswith("/api/status"):
            self.handle_api_status()
        elif self.path.startswith("/api/download-zip"):
            self.handle_download_zip()
        elif self.path.startswith("/api/files"):
            self.handle_api_files()
        elif path_only in ("/preview", "/preview/"):
            self.handle_preview("index.html")
        elif self.path.startswith("/preview/"):
            rel_name = self.path[len("/preview/"):].split("?")[0]
            self.handle_preview(rel_name or "index.html")
        else:
            # Fallback to default static file handling
            super().do_GET()


    def do_POST(self):
        """Handle POST requests for generation control and authentication."""
        if self.path.startswith("/api/auth/signup"):
            self.handle_auth_signup()
        elif self.path.startswith("/api/auth/login"):
            self.handle_auth_login()
        elif self.path.startswith("/api/generate"):
            self.handle_api_generate()
        elif self.path.startswith("/api/reset"):
            self.handle_api_reset()
        else:
            self.send_error(404, "Endpoint not found")

    def serve_file(self, filepath: Path, content_type: str):
        """Serve a static file from disk."""
        if not filepath.exists():
            self.send_error(404, f"File not found: {filepath.name}")
            return
        content = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, data: dict, status_code: int = 200):
        """Send a JSON response."""
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def handle_api_status(self):
        """Return the current generation state and live timers."""
        with pipeline_lock:
            state_copy = dict(generation_state)
            if state_copy["is_running"]:
                state_copy["elapsed_seconds"] = round(time.time() - state_copy["start_time"], 2)
                # Update current running step duration
                current_id = state_copy.get("current_step_id")
                updated_steps = []
                for s in state_copy["steps"]:
                    sc = dict(s)
                    if sc["status"] == "running" and sc["start_time"] > 0:
                        sc["duration"] = round(time.time() - sc["start_time"], 2)
                    updated_steps.append(sc)
                state_copy["steps"] = updated_steps
        self.send_json(state_copy)

    def get_request_user_id(self) -> str:
        """Extract user_id from Authorization Bearer token, query parameter, cookie, or active generation."""
        # 1. Check Authorization: Bearer <jwt>
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            from tools.project.storage import auth_get_user
            u = auth_get_user(token)
            if u and u.get("user_id"):
                return u["user_id"]

        # 2. Check query parameter ?user_id=...
        if "?" in self.path:
            query = self.path.split("?", 1)[1]
            for param in query.split("&"):
                if param.startswith("user_id="):
                    val = param.split("=", 1)[1].strip()
                    if val:
                        return val

        # 3. Check Cookie: devpilot_user_id=...
        cookie_header = self.headers.get("Cookie", "")
        if "devpilot_user_id=" in cookie_header:
            for part in cookie_header.split(";"):
                part = part.strip()
                if part.startswith("devpilot_user_id="):
                    val = part.split("=", 1)[1].strip()
                    if val:
                        return val

        # 4. Fallback: check active generation state user_id
        with pipeline_lock:
            active_uid = generation_state.get("user_id")
            if active_uid and active_uid != "default":
                return active_uid

        # 5. Fallback: check if there is an existing user workspace in generated_project/users/
        users_dir = PROJECT_ROOT_DIR / "generated_project" / "users"
        if users_dir.exists():
            u_dirs = [d.name for d in users_dir.iterdir() if d.is_dir()]
            if u_dirs:
                return u_dirs[-1]

        return "default"

    def handle_auth_signup(self):
        """Register a new user via Supabase Auth."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except Exception:
            self.send_json({"error": "Invalid JSON"}, status_code=400)
            return

        email = payload.get("email", "").strip()
        password = payload.get("password", "").strip()
        if not email or not password:
            self.send_json({"error": "Email and password are required"}, status_code=400)
            return

        from tools.project.storage import auth_sign_up
        result = auth_sign_up(email, password)
        status = 200 if result.get("success") else 400
        self.send_json(result, status_code=status)

    def handle_auth_login(self):
        """Sign in a user via Supabase Auth."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except Exception:
            self.send_json({"error": "Invalid JSON"}, status_code=400)
            return

        email = payload.get("email", "").strip()
        password = payload.get("password", "").strip()
        if not email or not password:
            self.send_json({"error": "Email and password are required"}, status_code=400)
            return

        from tools.project.storage import auth_sign_in
        result = auth_sign_in(email, password)
        status = 200 if result.get("success") else 401
        self.send_json(result, status_code=status)

    def handle_auth_me(self):
        """Validate session token and return user details."""
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            self.send_json({"authenticated": False}, status_code=401)
            return

        token = auth_header[7:].strip()
        from tools.project.storage import auth_get_user
        u = auth_get_user(token)
        if u:
            self.send_json({"authenticated": True, "user": u})
        else:
            self.send_json({"authenticated": False}, status_code=401)

    def handle_api_generate(self):
        """Start a new generation run in a background thread."""
        with pipeline_lock:
            if generation_state["is_running"]:
                self.send_json({"error": "Generation is already in progress."}, status_code=400)
                return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON body."}, status_code=400)
            return

        prompt = payload.get("prompt", "").strip()
        clean = payload.get("clean", True)
        user_id = payload.get("user_id") or self.get_request_user_id()

        if not prompt:
            self.send_json({"error": "Prompt cannot be empty."}, status_code=400)
            return

        reset_generation_state()
        with pipeline_lock:
            generation_state["is_running"] = True
            generation_state["status"] = "RUNNING"
            generation_state["start_time"] = time.time()
            generation_state["prompt"] = prompt
            generation_state["user_id"] = user_id

        # Launch agent pipeline in background thread with user_id
        thread = threading.Thread(
            target=run_agent_pipeline,
            args=(prompt, clean, user_id),
            daemon=True,
        )
        thread.start()

        self.send_json({"message": "Generation started.", "prompt": prompt, "user_id": user_id})

    def handle_api_reset(self):
        """Reset generation state."""
        with pipeline_lock:
            if generation_state["is_running"]:
                self.send_json({"error": "Cannot reset while running."}, status_code=400)
                return
        reset_generation_state()
        self.send_json({"message": "State reset."})

    def handle_download_zip(self):
        """Package and stream ZIP directly from Supabase Cloud Storage for the active user."""
        from tools.project.storage import build_cloud_zip_buffer
        from tools.project.workspace import get_user_workspace_root

        user_id = self.get_request_user_id()
        zip_data = None

        # 1. Attempt to build ZIP directly from Supabase Storage for this user
        try:
            zip_data = build_cloud_zip_buffer(user_id=user_id)
            if zip_data:
                print(f"  [OK] Streaming project ZIP for user [{user_id}] from Supabase Storage bucket!")
        except Exception as exc:
            print(f"  [WARN] Cloud ZIP fetch failed ({exc}), falling back to local files.")

        # 2. Fallback to local files if cloud bucket was empty or unreachable
        if not zip_data:
            user_root = get_user_workspace_root(user_id)
            if not user_root.exists():
                self.send_error(404, "No generated project found to download.")
                return

            zip_buffer = io.BytesIO()
            files_count = 0
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for file_path in user_root.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(user_root)
                        zf.write(file_path, arcname=arcname)
                        files_count += 1

            if files_count == 0:
                self.send_error(404, "Generated project directory is empty.")
                return

            zip_data = zip_buffer.getvalue()

        zip_filename = f"generated_project_{user_id[:8]}.zip"

        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", f'attachment; filename="{zip_filename}"')
        self.send_header("Content-Length", str(len(zip_data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(zip_data)

    def handle_api_files(self):
        """Return list of files and content for preview, sourced from Supabase Storage for the active user."""
        from tools.project.storage import list_cloud_files, download_cloud_file
        from tools.project.workspace import get_user_workspace_root

        user_id = self.get_request_user_id()
        files = []
        try:
            cloud_files = list_cloud_files(user_id=user_id)
            for cf in cloud_files:
                name = cf.get("name")
                if not name:
                    continue
                raw_bytes = download_cloud_file(name, user_id=user_id)
                content = raw_bytes.decode("utf-8", errors="replace") if raw_bytes else ""
                files.append({
                    "name": name,
                    "size": len(raw_bytes) if raw_bytes else 0,
                    "content": content[:20000],
                })
        except Exception:
            pass

        # Fallback to local user workspace if cloud listing returned empty
        user_root = get_user_workspace_root(user_id)
        if not files and user_root.exists():
            for f in sorted(user_root.rglob("*")):
                if f.is_file():
                    rel = str(f.relative_to(user_root))
                    try:
                        content = f.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        content = "[Binary file]"
                    files.append({
                        "name": rel,
                        "size": f.stat().st_size,
                        "content": content[:20000],  # cap preview
                    })

        self.send_json({"files": files})

    def handle_preview(self, filename: str = "index.html"):
        """Serve generated project files for live browser sandbox preview for the active user."""
        from tools.project.storage import download_cloud_file
        from tools.project.workspace import get_user_workspace_root

        user_id = self.get_request_user_id()
        raw_bytes = None

        # 1. Try Supabase Storage first under users/{user_id}/...
        try:
            raw_bytes = download_cloud_file(filename, user_id=user_id)
        except Exception:
            pass

        # 2. Fallback to local workspace files
        if raw_bytes is None:
            user_root = get_user_workspace_root(user_id)
            local_path = user_root / filename
            if local_path.exists() and local_path.is_file():
                try:
                    raw_bytes = local_path.read_bytes()
                except Exception:
                    pass

        if raw_bytes is None:
            self.send_error(404, f"Preview file not found: {filename}")
            return

        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        content_types = {
            "html": "text/html",
            "css": "text/css",
            "js": "application/javascript",
            "json": "application/json",
            "png": "image/png",
            "jpg": "image/jpeg",
            "svg": "image/svg+xml",
            "ico": "image/x-icon",
        }
        content_type = content_types.get(ext, "text/plain")

        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(raw_bytes)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Set-Cookie", f"devpilot_user_id={user_id}; Path=/preview/; SameSite=Lax")
        self.end_headers()
        self.wfile.write(raw_bytes)



# Configure UTF-8 on Windows stdout/stderr
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_server(port: int = 10000):
    """Start the multi-threaded HTTP server."""
    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, NeonGeneratorHandler)
    httpd.daemon_threads = True
    print("\n" + "=" * 65)
    print(">> NEON PROJECT GENERATOR -- WEB SERVER RUNNING (MULTI-THREADED)")
    print(f">> Local URL : http://localhost:{port}")
    print(f">> Serving   : {STATIC_DIR}")
    print("=" * 65 + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Neon Generator Web Server")
    default_port = int(os.getenv("PORT", 10000))
    parser.add_argument("--port", type=int, default=default_port, help=f"Port to listen on (default: {default_port})")
    args = parser.parse_args()
    run_server(port=args.port)
