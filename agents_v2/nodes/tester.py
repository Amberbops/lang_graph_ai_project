"""
Tester Node — DevPilot agents_v2.

Responsibility:
    Validate the current project implementation.

The Tester:

    1. Discovers the project's available validation mechanism.
    2. Executes the appropriate test/build/static-validation command.
    3. Captures stdout, stderr, and exit code.
    4. Uses a fast LLM only to parse human-readable test output.
    5. Uses the command exit code as the authoritative success signal.
    6. Stores a structured TestResult in AgentState.

Possible final statuses:

    TESTS_PASSED
    TESTS_FAILED
    VALIDATION_PASSED
    VALIDATION_FAILED
    NO_TESTS
    TEST_ERROR
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents_v2.models import get_fast_model
from agents_v2.states import AgentState

from tools.filesystem.operations import list_files
from tools.terminal.executor import run_cmd

from tools.project.workspace import PROJECT_ROOT


# ==================================================================
# STRUCTURED TEST RESULT
# ==================================================================


class TestResult(BaseModel):
    """Structured result produced by the Tester."""

    runner: str = Field(
        description=(
            "Validation runner used, such as pytest, jest, "
            "vitest, mocha, npm, unittest, static, or none."
        )
    )

    validation_type: str = Field(
        description=(
            "Type of validation performed: TESTS, BUILD, "
            "STATIC, or NONE."
        )
    )

    passed: int = Field(
        default=0,
        description="Number of tests reported as passed.",
    )

    failed: int = Field(
        default=0,
        description="Number of tests reported as failed.",
    )

    errors: List[str] = Field(
        default_factory=list,
        description=(
            "Concise error messages or important failure information."
        ),
    )

    summary: str = Field(
        description=(
            "Concise human-readable summary of the validation result."
        )
    )

    success: bool = Field(
        description=(
            "Parser interpretation of whether validation succeeded. "
            "The application will independently verify this using "
            "the process exit code."
        )
    )


# ==================================================================
# PARSER PROMPT
# ==================================================================


tester_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are DevPilot's Test Result Parser.

Your task is to analyze the raw output produced by a project's
test or validation command.

Extract:

1. The validation runner.
2. The number of passed tests, when explicitly reported.
3. The number of failed tests, when explicitly reported.
4. Important errors or failure messages.
5. A concise summary.
6. Whether the output appears successful.

IMPORTANT:

- Do NOT invent test counts.
- If a count is not explicitly available, use 0.
- Keep error messages concise.
- Do not invent test names or failures.
- Do not claim tests passed merely because the command output
  looks clean.
- Treat the return code as additional evidence, not something
  to override with invented information.

The application will separately use the actual process return
code as the authoritative success signal.
""",
        ),
        (
            "human",
            """
PROJECT FILES:
{project_files}

VALIDATION COMMAND:
{test_command}

VALIDATION TYPE:
{validation_type}

STDOUT:
{stdout}

STDERR:
{stderr}

RETURN CODE:
{returncode}
""",
        ),
    ]
)


# ==================================================================
# PROJECT HELPERS
# ==================================================================


def _read_package_json() -> Dict[str, Any]:
    """
    Read package.json safely.
    """

    package_path = (
        Path(PROJECT_ROOT)
        / "package.json"
    )

    if not package_path.exists():
        return {}

    if not package_path.is_file():
        return {}

    try:
        return json.loads(
            package_path.read_text(
                encoding="utf-8"
            )
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return {}


def _has_file_pattern(
    patterns: List[str],
) -> bool:
    """
    Check whether any file matching the supplied glob patterns
    exists in the project.
    """

    root = Path(PROJECT_ROOT)

    for pattern in patterns:

        if any(root.glob(pattern)):
            return True

    return False


def _has_python_tests() -> bool:
    """
    Detect common Python test files.
    """

    root = Path(PROJECT_ROOT)

    if any(
        root.rglob("test_*.py")
    ):
        return True

    if any(
        root.rglob("*_test.py")
    ):
        return True

    # Common Python test configuration files.
    for filename in [
        "pytest.ini",
        "tox.ini",
        "unittest.cfg",
    ]:

        if (
            root / filename
        ).exists():

            return True

    return False


def _detect_npm_test_runner(
    package_data: Dict[str, Any],
) -> Optional[Tuple[str, str, str]]:
    """
    Detect a JavaScript/TypeScript test command.

    Returns:
        (command, runner, validation_type)
    """

    scripts = package_data.get(
        "scripts",
        {},
    )

    dependencies = {
        **package_data.get(
            "dependencies",
            {},
        ),
        **package_data.get(
            "devDependencies",
            {},
        ),
    }

    # --------------------------------------------------------------
    # Explicit npm test script gets highest priority.
    # --------------------------------------------------------------

    if "test" in scripts:

        test_script = str(
            scripts["test"]
        )

        # Try to identify the actual runner.
        script_lower = test_script.lower()

        if "vitest" in script_lower:
            runner = "vitest"

        elif "jest" in script_lower:
            runner = "jest"

        elif "mocha" in script_lower:
            runner = "mocha"

        elif "ava" in script_lower:
            runner = "ava"

        else:
            runner = "npm"

        return (
            "npm test",
            runner,
            "TESTS",
        )

    # --------------------------------------------------------------
    # Vitest dependency
    # --------------------------------------------------------------

    if "vitest" in dependencies:

        return (
            "npx vitest run",
            "vitest",
            "TESTS",
        )

    # --------------------------------------------------------------
    # Jest dependency
    # --------------------------------------------------------------

    if "jest" in dependencies:

        return (
            "npx jest --runInBand --no-coverage",
            "jest",
            "TESTS",
        )

    # --------------------------------------------------------------
    # Mocha dependency
    # --------------------------------------------------------------

    if "mocha" in dependencies:

        return (
            "npx mocha",
            "mocha",
            "TESTS",
        )

    return None


# ==================================================================
# VALIDATION DETECTION
# ==================================================================


def detect_validation_command() -> Tuple[
    Optional[str],
    str,
    str,
]:
    """
    Detect the most appropriate validation command.

    Returns:

        (
            command,
            runner,
            validation_type
        )

    Examples:

        (
            "pytest --tb=short -q",
            "pytest",
            "TESTS"
        )

        (
            "npm test",
            "vitest",
            "TESTS"
        )

        (
            "npm run build",
            "npm",
            "BUILD"
        )

        (
            None,
            "none",
            "NONE"
        )
    """

    root = Path(PROJECT_ROOT)

    # ==============================================================
    # Python tests
    # ==============================================================

    if _has_python_tests():

        return (
            "pytest --tb=short -q",
            "pytest",
            "TESTS",
        )

    # ==============================================================
    # Python unittest
    # ==============================================================

    if _has_file_pattern(
        [
            "test*.py",
            "tests/*.py",
            "tests/**/*.py",
        ]
    ):

        return (
            "python -m unittest discover",
            "unittest",
            "TESTS",
        )

    # ==============================================================
    # JavaScript / TypeScript
    # ==============================================================

    package_data = _read_package_json()

    if package_data:

        npm_validation = (
            _detect_npm_test_runner(
                package_data
            )
        )

        if npm_validation is not None:

            return npm_validation

        # ----------------------------------------------------------
        # No test suite but build script exists.
        # ----------------------------------------------------------

        scripts = package_data.get(
            "scripts",
            {},
        )

        if "build" in scripts:

            return (
                "npm run build",
                "npm",
                "BUILD",
            )

    # ==============================================================
    # Static JavaScript validation
    # ==============================================================

    script_path = root / "script.js"

    if script_path.exists():

        return (
            "node --check script.js",
            "node",
            "STATIC",
        )

    # ==============================================================
    # No supported validation
    # ==============================================================

    return (
        None,
        "none",
        "NONE",
    )


# ==================================================================
# OUTPUT NORMALIZATION
# ==================================================================


def _normalize_command_result(
    result: Any,
) -> Tuple[int, str, str]:
    """
    Normalize run_cmd output.
    """

    if (
        isinstance(result, tuple)
        and len(result) == 3
    ):

        return (
            int(result[0]),
            str(result[1]),
            str(result[2]),
        )

    return (
        1,
        "",
        (
            "Unexpected result returned by "
            f"run_cmd: {result}"
        ),
    )


# ==================================================================
# MAIN TESTER
# ==================================================================


def tester_node(
    state: AgentState,
) -> AgentState:
    """
    Run project validation and store a structured result.
    """

    # ==============================================================
    # Gather actual project files
    # ==============================================================

    try:

        project_files = list_files.invoke(
            {
                "directory": "."
            }
        )

    except Exception as exc:

        return {
            **state,
            "status": "TEST_ERROR",
            "test_results": {
                "runner": "none",
                "validation_type": "NONE",
                "passed": 0,
                "failed": 0,
                "errors": [
                    str(exc)
                ],
                "summary": (
                    "The Tester could not inspect "
                    "the project files."
                ),
                "success": False,
            },
            "errors": [
                *state.get(
                    "errors",
                    []
                ),
                str(exc),
            ],
        }

    # ==============================================================
    # Detect validation command
    # ==============================================================

    (
        test_command,
        detected_runner,
        validation_type,
    ) = detect_validation_command()

    # ==============================================================
    # No validation mechanism
    # ==============================================================

    if test_command is None:

        result = {
            "runner": "none",
            "validation_type": "NONE",
            "passed": 0,
            "failed": 0,
            "errors": [],
            "summary": (
                "No supported automated test or "
                "validation command was detected."
            ),
            "success": False,
        }

        return {
            **state,
            "test_results": result,
            "status": "NO_TESTS",
        }

    # ==============================================================
    # Execute validation
    # ==============================================================

    try:

        raw_result = run_cmd.invoke(
            {
                "cmd": test_command,
            }
        )

        (
            returncode,
            stdout,
            stderr,
        ) = _normalize_command_result(
            raw_result
        )

    except Exception as exc:

        result = {
            "runner": detected_runner,
            "validation_type": validation_type,
            "passed": 0,
            "failed": 0,
            "errors": [
                str(exc)
            ],
            "summary": (
                "The validation command could not "
                "be executed."
            ),
            "success": False,
        }

        return {
            **state,
            "test_results": result,
            "status": "TEST_ERROR",
            "errors": [
                *state.get(
                    "errors",
                    []
                ),
                str(exc),
            ],
        }

    # ==============================================================
    # Parse output with fast model
    #
    # This is interpretation only.
    # Exit code remains authoritative.
    # ==============================================================

    try:

        model = get_fast_model()

        structured_model = (
            model.with_structured_output(
                TestResult
            )
        )

        chain = (
            tester_parse_prompt
            | structured_model
        )

        parsed: TestResult = chain.invoke(
            {
                "project_files": project_files,
                "test_command": test_command,
                "validation_type": validation_type,
                "stdout": stdout[:6000],
                "stderr": stderr[:4000],
                "returncode": str(returncode),
            }
        )

        parsed_dict = parsed.model_dump()

    except Exception as exc:

        # ----------------------------------------------------------
        # Parser failure must not erase the actual command result.
        # ----------------------------------------------------------

        parsed_dict = {
            "runner": detected_runner,
            "validation_type": validation_type,
            "passed": 0,
            "failed": 0,
            "errors": [
                (
                    "Test output parser failed: "
                    f"{type(exc).__name__}: {exc}"
                )
            ],
            "summary": (
                "Validation command completed, but its "
                "output could not be parsed."
            ),
            "success": False,
        }

    # ==============================================================
    # AUTHORITATIVE RESULT
    # ==============================================================
    #
    # The process return code determines success.
    #
    # The model cannot turn exit code 1 into success=True.
    # ==============================================================

    if validation_type == "TESTS":

        actual_success = (
            returncode == 0
        )

        if actual_success:

            final_status = (
                "TESTS_PASSED"
            )

        else:

            final_status = (
                "TESTS_FAILED"
            )

    elif validation_type in {
        "BUILD",
        "STATIC",
    }:

        actual_success = (
            returncode == 0
        )

        if actual_success:

            final_status = (
                "VALIDATION_PASSED"
            )

        else:

            final_status = (
                "VALIDATION_FAILED"
            )

    else:

        actual_success = (
            returncode == 0
        )

        final_status = (
            "VALIDATION_PASSED"
            if actual_success
            else "VALIDATION_FAILED"
        )

    # ==============================================================
    # Ensure execution failure is visible in errors
    # ==============================================================

    execution_errors = list(
        parsed_dict.get(
            "errors",
            [],
        )
    )

    if returncode != 0:

        execution_errors.append(
            (
                f"Command exited with code "
                f"{returncode}."
            )
        )

        if stderr.strip():

            execution_errors.append(
                stderr[:3000]
            )

    # Deduplicate errors.
    execution_errors = list(
        dict.fromkeys(
            execution_errors
        )
    )

    # ==============================================================
    # Final structured result
    # ==============================================================

    final_result = {
        **parsed_dict,

        "runner": detected_runner,

        "validation_type": validation_type,

        "success": actual_success,

        "exit_code": returncode,

        "command": test_command,

        "stdout": stdout[:6000],

        "stderr": stderr[:4000],

        "errors": execution_errors,
    }

    # ==============================================================
    # Update AgentState
    # ==============================================================

    return {
        **state,

        "test_results": final_result,

        "errors": [
            *state.get(
                "errors",
                []
            ),
            *execution_errors,
        ],

        "status": final_status,
    }