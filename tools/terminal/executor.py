import subprocess
from typing import Tuple

from langchain_core.tools import tool

from tools.project.workspace import (
    PROJECT_ROOT,
    safe_path_for_project,
)


@tool
def run_cmd(
    cmd: str,
    cwd: str = "",
    timeout: int = 30,
) -> Tuple[int, str, str]:
    """
    Run a shell command inside the generated project.
    """

    cwd_dir = (
        safe_path_for_project(cwd)
        if cwd
        else PROJECT_ROOT
    )

    result = subprocess.run(
        cmd,
        shell=True,
        cwd=str(cwd_dir),
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    return (
        result.returncode,
        result.stdout,
        result.stderr,
    )