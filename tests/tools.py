import shutil
import tempfile
from pathlib import Path

from tools.project.workspace import (
    PROJECT_ROOT,
    safe_path_for_project,
)

from tools.filesystem.operations import (
    write_file,
    read_file,
    list_files,
)

from tools.terminal.executor import run_cmd


def make_test_workspace():
    """
    Create a temporary workspace for tests.

    This prevents tests from modifying the real
    generated_project directory.
    """

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="devpilot_test_"
        )
    )

    return temp_dir


def cleanup_test_workspace(path: Path):
    """
    Remove the temporary workspace.
    """

    if path.exists():
        shutil.rmtree(path)


def test_path_traversal_is_blocked():
    """
    Test path traversal against the real workspace root logic.

    Does not create or modify generated_project.
    """

    try:
        safe_path_for_project("../outside.txt")

    except ValueError:
        return

    raise AssertionError(
        "Path traversal was not blocked."
    )


def test_project_root_exists():
    """
    Verify the configured project root path is valid.
    """

    assert PROJECT_ROOT.name == "generated_project"


def test_safe_path_stays_inside_project():
    """
    Verify normal project paths resolve safely.
    """

    result = safe_path_for_project(
        "src/app.js"
    )

    root = PROJECT_ROOT.resolve()
    resolved = result.resolve()

    assert (
        resolved == root
        or root in resolved.parents
    )