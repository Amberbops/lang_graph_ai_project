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
from http.server import HTTPServer, SimpleHTTPRequestHandler
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

def run_agent_pipeline(prompt: str, clean_workspace: bool = True):
    """Execute DevPilot LangGraph chain with live step timers."""
    try:
        from agents_v2.graph import app

        with pipeline_lock:
            generation_state["is_running"] = True
            generation_state["status"] = "RUNNING"
            generation_state["start_time"] = time.time()
            generation_state["prompt"] = prompt

        log_event(f"Starting agent pipeline for prompt: \"{prompt}\"")

        if clean_workspace:
            log_event("Cleaning generated_project workspace directory...", "info")
            init_project_root(clean=True)
            log_event("Workspace cleared.", "info")
        else:
            init_project_root(clean=False)

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

        for chunk in app.stream(initial_state, {"recursion_limit": 150}):
            for node_name, state_update in chunk.items():
                log_event(f"Completed node: {node_name}", "info")
                update_step(node_name, "completed")

                # Advance to next logical step
                if node_name == "router":
                    intent = state_update.get("intent", "CREATE")
                    log_event(f"Intent classified: {intent}")
                    update_step("inspector", "running")
                elif node_name == "inspector":
                    update_step("architect", "running")
                elif node_name == "architect":
                    arch = state_update.get("architecture", {})
                    summary = arch.get("summary", "Architecture designed.")
                    log_event(f"Architecture ready: {summary[:100]}...")
                    update_step("planner", "running")
                elif node_name == "planner":
                    plan = state_update.get("plan", {})
                    goal = plan.get("goal", "Plan ready.")
                    log_event(f"Plan ready: {goal[:100]}...")
                    update_step("coder", "running")
                elif node_name == "coder":
                    files = state_update.get("files_changed", [])
                    log_event(f"Coder active. Files changed so far: {len(files)}")
                    if state_update.get("status") in ("CODER_DONE", "CODER_LIMIT_REACHED"):
                        update_step("coder", "completed")
                        update_step("tester", "running")
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

        # Inspect generated files
        files_list = []
        if PROJECT_ROOT.exists():
            for f in sorted(PROJECT_ROOT.rglob("*")):
                if f.is_file():
                    rel = str(f.relative_to(PROJECT_ROOT))
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
        log_event(f"✅ Project generation complete! {len(files_list)} files generated in {generation_state['elapsed_seconds']}s.", "success")

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
        if self.path == "/" or self.path == "/index.html":
            self.serve_file(STATIC_DIR / "index.html", "text/html")
        elif self.path == "/about" or self.path == "/about.html":
            self.serve_file(STATIC_DIR / "about.html", "text/html")
        elif self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        elif self.path == "/style.css":
            self.serve_file(STATIC_DIR / "style.css", "text/css")
        elif self.path == "/app.js":
            self.serve_file(STATIC_DIR / "app.js", "application/javascript")
        elif self.path.startswith("/api/status"):
            self.handle_api_status()
        elif self.path.startswith("/api/download-zip"):
            self.handle_download_zip()
        elif self.path.startswith("/api/files"):
            self.handle_api_files()
        else:
            # Fallback to default static file handling
            super().do_GET()


    def do_POST(self):
        """Handle POST requests for generation control."""
        if self.path.startswith("/api/generate"):
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

        if not prompt:
            self.send_json({"error": "Prompt cannot be empty."}, status_code=400)
            return

        reset_generation_state()

        # Launch agent pipeline in background thread
        thread = threading.Thread(
            target=run_agent_pipeline,
            args=(prompt, clean),
            daemon=True,
        )
        thread.start()

        self.send_json({"message": "Generation started.", "prompt": prompt})

    def handle_api_reset(self):
        """Reset generation state."""
        with pipeline_lock:
            if generation_state["is_running"]:
                self.send_json({"error": "Cannot reset while running."}, status_code=400)
                return
        reset_generation_state()
        self.send_json({"message": "State reset."})

    def handle_download_zip(self):
        """Package generated_project into a zip file and send as download."""
        if not PROJECT_ROOT.exists():
            self.send_error(404, "No generated project found to download.")
            return

        zip_buffer = io.BytesIO()
        files_count = 0

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in PROJECT_ROOT.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(PROJECT_ROOT)
                    zf.write(file_path, arcname=arcname)
                    files_count += 1

        if files_count == 0:
            self.send_error(404, "Generated project directory is empty.")
            return

        zip_data = zip_buffer.getvalue()
        zip_filename = "generated_project.zip"

        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", f'attachment; filename="{zip_filename}"')
        self.send_header("Content-Length", str(len(zip_data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(zip_data)

    def handle_api_files(self):
        """Return list of files and content for preview."""
        if not PROJECT_ROOT.exists():
            self.send_json({"files": []})
            return

        files = []
        for f in sorted(PROJECT_ROOT.rglob("*")):
            if f.is_file():
                rel = str(f.relative_to(PROJECT_ROOT))
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


# Configure UTF-8 on Windows stdout/stderr
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_server(port: int = 5000):
    """Start the multi-threaded HTTP server."""
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, NeonGeneratorHandler)
    print("\n" + "=" * 65)
    print(">> NEON PROJECT GENERATOR -- WEB SERVER RUNNING")
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
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    args = parser.parse_args()
    run_server(port=args.port)
