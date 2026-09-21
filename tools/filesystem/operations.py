import shutil
from langchain_core.tools import tool

from tools.project.workspace import (
    PROJECT_ROOT,
    safe_path_for_project,
)


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file inside the generated project."""

    file_path = safe_path_for_project(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    return f"WROTE: {file_path}"


@tool
def read_file(path: str) -> str:
    """Read a file from the generated project."""

    file_path = safe_path_for_project(path)

    if not file_path.exists():
        return f"File not found: {path}"

    if not file_path.is_file():
        return f"Not a file: {path}"

    return file_path.read_text(encoding="utf-8")


@tool
def list_files(directory: str = ".") -> str:

    """List all files inside the generated project."""

    directory_path = safe_path_for_project(directory)

    if not directory_path.exists():
        return "Directory not found."

    files = [
        str(file.relative_to(PROJECT_ROOT))
        for file in directory_path.rglob("*")
        if file.is_file()
    ]

    return "\n".join(files) if files else "No files found."


@tool
def delete_file(path: str) -> str:
    """Delete a file or subfolder inside the generated project."""
    file_path = safe_path_for_project(path)
    if not file_path.exists():
        return f"File not found: {path}"
    if file_path == PROJECT_ROOT.resolve():
        return "Cannot delete project root directly. Use clear_workspace instead."
    if file_path.is_dir():
        shutil.rmtree(file_path)
        return f"DELETED DIRECTORY: {path}"
    file_path.unlink()
    return f"DELETED: {path}"


@tool
def clear_workspace() -> str:
    """Clear all files and subdirectories from the generated project workspace."""
    if PROJECT_ROOT.exists():
        for item in PROJECT_ROOT.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return "WORKSPACE CLEARED."