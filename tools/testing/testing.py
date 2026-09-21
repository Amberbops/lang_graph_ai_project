"""
Testing tools — available to any agent that needs to run tests.

Currently wraps the run_cmd tool with convenience logic for
common test runners (pytest, jest).
"""

from langchain_core.tools import tool

from tools.terminal.executor import run_cmd
from tools.project.workspace import PROJECT_ROOT


@tool
def run_tests(runner: str = "auto") -> str:
    """
    Run the project's test suite.

    Args:
        runner: 'auto' (default), 'pytest', 'jest', or 'none'.

    Returns a string containing the full test output (stdout + stderr).
    """

    root = PROJECT_ROOT

    if runner == "auto":
        has_pytest = any(root.rglob("test_*.py")) or any(
            root.rglob("*_test.py")
        )
        has_jest = (root / "package.json").exists()

        if has_pytest:
            runner = "pytest"
        elif has_jest:
            runner = "jest"
        else:
            return "No test files detected. Nothing to run."

    if runner == "pytest":
        returncode, stdout, stderr = run_cmd.invoke(
            {"cmd": "pytest --tb=short -q"}
        )
        return (
            f"Exit code: {returncode}\n\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )

    if runner == "jest":
        returncode, stdout, stderr = run_cmd.invoke(
            {"cmd": "npx jest --no-coverage"}
        )
        return (
            f"Exit code: {returncode}\n\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )

    return f"Unknown runner: {runner}. Use 'auto', 'pytest', or 'jest'."
