from pathlib import Path
import shutil
from sys import path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = REPO_ROOT / "generated_project"

def init_project_root(clean: bool = True)->Path:
    """Create the generated project Workspace."""
    if clean and PROJECT_ROOT.exists():
        shutil.rmtree(PROJECT_ROOT)
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return PROJECT_ROOT

def safe_path_for_project(path: str = "")->Path:
    """
    Resolve a Path safely inside generated_project.
    
    Prevents path traversal outside the project workspace.
    """
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    if not path or path.strip() == "":
        return PROJECT_ROOT
    
    root=PROJECT_ROOT.resolve()
    candidate=(PROJECT_ROOT / path).resolve()

    if candidate != root and root not in candidate.parents:
        raise ValueError(
            f"Attempt to access outside project root.\n"
            f"root={root}\n"
            f"candidate={candidate}"
        )
    return candidate

def get_current_directory() -> Path:
    """Return the absolute project workspace path."""
    return str(PROJECT_ROOT.resolve())