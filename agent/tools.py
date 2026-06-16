import pathlib
import subprocess
from typing import Tuple
from langchain_core.tools import tool

PROJECT_ROOT = (
    pathlib.Path(__file__).resolve().parent.parent
    / "generated_project"
)


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    print("PROJECT_ROOT =", PROJECT_ROOT.resolve())
    return PROJECT_ROOT


def safe_path_for_project(path: str) -> pathlib.Path:
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    if not path or path.strip() == "":
        return PROJECT_ROOT

    candidate = (PROJECT_ROOT / path).resolve()
    root = PROJECT_ROOT.resolve()

    if root != candidate and root not in candidate.parents:
        raise ValueError(
            f"Attempt to access outside project root.\n"
            f"root={root}\n"
            f"candidate={candidate}"
        )

    return candidate


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file inside the generated project."""
    p = safe_path_for_project(path)

    p.parent.mkdir(parents=True, exist_ok=True)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"WROTE: {p}"


@tool
def read_file(path: str) -> str:
    """Read a file from the generated project."""
    p = safe_path_for_project(path)

    if not p.exists():
        return ""

    return p.read_text(encoding="utf-8")


@tool
def list_files(directory: str = ".") -> str:
    """List all files inside the generated project."""

    if not directory:
        directory = "."

    p = safe_path_for_project(directory)

    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    files = [
        str(f.relative_to(PROJECT_ROOT))
        for f in p.rglob("*")
        if f.is_file()
    ]

    return "\n".join(files) if files else "No files found."


@tool
def get_current_directory() -> str:
    """Return project root directory."""
    return str(PROJECT_ROOT)


@tool
def run_cmd(cmd: str, cwd: str = "", timeout: int = 30) -> Tuple[int, str, str]:
    """Run a shell command inside the project root."""

    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT

    res = subprocess.run(
        cmd,
        shell=True,
        cwd=str(cwd_dir),
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    return res.returncode, res.stdout, res.stderr