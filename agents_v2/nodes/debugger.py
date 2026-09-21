"""
Debugger Node — DevPilot agents_v2.

Responsibility:

    Analyze a reported software bug or failed validation result
    and produce a structured diagnosis and fix plan.

The Debugger does NOT modify project files.

The Coder receives the Debugger's output and performs the actual fix.
"""

import json
from typing import List, Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents_v2.models import get_reasoning_model
from agents_v2.states import AgentState


# ==================================================================
# STRUCTURED DEBUG RESULT
# ==================================================================


Severity = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
]


class DebugAnalysis(BaseModel):
    """
    Structured diagnosis produced by the Debugger.
    """

    problem: str = Field(
        description=(
            "Clear description of the bug or validation failure."
        )
    )

    root_cause: str = Field(
        description=(
            "Most likely root cause based only on available evidence."
        )
    )

    severity: Severity = Field(
        description=(
            "Severity of the issue."
        )
    )

    evidence: List[str] = Field(
        default_factory=list,
        description=(
            "Concrete evidence supporting the diagnosis."
        )
    )

    affected_files: List[str] = Field(
        default_factory=list,
        description=(
            "Files likely involved in the problem."
        )
    )

    fix_tasks: List[str] = Field(
        default_factory=list,
        description=(
            "Ordered implementation actions the Coder should perform "
            "to fix the issue."
        )
    )

    validation_steps: List[str] = Field(
        default_factory=list,
        description=(
            "Steps that should be used to verify the fix."
        )
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Confidence in the diagnosis, from 0 to 1."
        )
    )


# ==================================================================
# DEBUGGER PROMPT
# ==================================================================


debugger_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are DevPilot's Debugger Agent.

Your responsibility is to diagnose a software bug or failed
validation and create a precise fix plan for the Coding Agent.

You do NOT modify files.

============================================================
IMPORTANT
============================================================

Use ONLY evidence provided in the input.

Do not invent:
- files
- error messages
- stack traces
- dependencies
- framework behavior
- test results
- code that was not shown

If the root cause cannot be determined with certainty, describe
the most likely cause and lower the confidence score.

============================================================
DEBUGGING PROCESS
============================================================

1. Identify the reported problem.
2. Examine test failures and command output when available.
3. Compare the failure with the project inspection.
4. Identify the most likely root cause.
5. Identify affected files.
6. Create ordered fix tasks for the Coder.
7. Define how the fix should be validated.

============================================================
WHEN TESTS FAILED
============================================================

Treat the actual command output and exit code as the strongest
evidence.

Do not ignore compiler errors, runtime errors, stack traces,
or failing test information.

============================================================
WHEN THERE ARE NO TEST RESULTS
============================================================

Use:
- the user's bug report
- project inspection
- previous errors
- available project context

Do not pretend that tests were executed.

============================================================
FIX TASK RULES
============================================================

Fix tasks must:

- be concrete
- be ordered
- focus only on the problem
- identify relevant files when possible
- avoid unrelated refactoring
- preserve existing behavior
- be directly executable by a Coding Agent

Do NOT write the actual code.

Return only the structured debugging analysis.
""",
        ),
        (
            "human",
            """
USER REQUEST:
{user_request}

INTENT:
{intent}

PROJECT INSPECTION:
{project_structure}

TEST RESULTS:
{test_results}

PREVIOUS ERRORS:
{errors}

CURRENT IMPLEMENTATION PLAN:
{plan}
""",
        ),
    ]
)


# ==================================================================
# DEBUGGER NODE
# ==================================================================


def debugger_node(
    state: AgentState,
) -> AgentState:
    """
    Diagnose the current bug/failure and produce a structured
    fix plan for the Coder.
    """

    user_request = state.get(
        "user_request",
        "",
    )

    intent = state.get(
        "intent",
        "DEBUG",
    )

    project_structure = state.get(
        "project_structure",
        "No project inspection available.",
    )

    test_results = state.get(
        "test_results",
    )

    errors = state.get(
        "errors",
        [],
    )

    plan = state.get(
        "plan",
    )

    # --------------------------------------------------------------
    # Limit potentially huge command output before giving it to
    # the reasoning model.
    # --------------------------------------------------------------

    if test_results:

        test_results_for_model = {
            **test_results,
            "stdout": str(
                test_results.get(
                    "stdout",
                    "",
                )
            )[:6000],
            "stderr": str(
                test_results.get(
                    "stderr",
                    "",
                )
            )[:4000],
        }

    else:

        test_results_for_model = {
            "status": "NO_TEST_RESULTS",
            "summary": (
                "No automated test result is available. "
                "Diagnose from the user's request and project context."
            ),
        }

    errors_for_model = [
        str(error)
        for error in errors
    ][-10:]

    plan_for_model = (
        plan
        if plan
        else {
            "goal": "No existing implementation plan",
            "tasks": [],
        }
    )

    # --------------------------------------------------------------
    # Reasoning model
    # --------------------------------------------------------------

    model = get_reasoning_model()

    structured_model = model.with_structured_output(
        DebugAnalysis
    )

    chain = (
        debugger_prompt
        | structured_model
    )

    try:

        analysis = chain.invoke(
            {
                "user_request": user_request,
                "intent": intent,
                "project_structure": project_structure,
                "test_results": json.dumps(
                    test_results_for_model,
                    indent=2,
                ),
                "errors": json.dumps(
                    errors_for_model,
                    indent=2,
                ),
                "plan": json.dumps(
                    plan_for_model,
                    indent=2,
                ),
            }
        )

    except Exception as exc:

        return {
            **state,

            "status": "DEBUGGER_FAILED",

            "debug_analysis": {
                "problem": (
                    "Debugger could not produce "
                    "a structured diagnosis."
                ),
                "root_cause": (
                    "Debugger execution failed."
                ),
                "severity": "HIGH",
                "evidence": [
                    str(exc)
                ],
                "affected_files": [],
                "fix_tasks": [],
                "validation_steps": [],
                "confidence": 0.0,
            },

            "errors": [
                *errors,
                (
                    "Debugger failed: "
                    f"{type(exc).__name__}: {exc}"
                ),
            ],
        }

    analysis_dict = analysis.model_dump()

    # --------------------------------------------------------------
    # Give the Coder a useful implementation plan for a direct
    # DEBUG request, even when there was no existing Planner output.
    # --------------------------------------------------------------

    current_plan = state.get(
        "plan"
    )

    if not current_plan:

        debug_tasks = []

        for index, task in enumerate(
            analysis.fix_tasks,
            start=1,
        ):
            debug_tasks.append(
                {
                    "id": index,
                    "title": f"Debug fix {index}",
                    "description": task,
                    "files": analysis.affected_files,
                    "priority": (
                        "CRITICAL"
                        if index == 1
                        else "HIGH"
                    ),
                    "required": True,
                    "depends_on": (
                        [index - 1]
                        if index > 1
                        else []
                    ),
                    "reasoning": (
                        "Required to resolve the diagnosed issue."
                    ),
                }
            )

        current_plan = {
            "goal": (
                f"Fix: {analysis.problem}"
            ),
            "approach": (
                analysis.root_cause
            ),
            "tasks": debug_tasks,
            "constraints": [
                "Preserve existing functionality.",
                "Change only files relevant to the bug.",
                "Validate the fix after implementation.",
            ],
        }

        task_state = debug_tasks

    else:

        task_state = state.get(
            "tasks",
            [],
        )

    # --------------------------------------------------------------
    # Return updated state
    # --------------------------------------------------------------

    return {
        **state,

        "debug_analysis": analysis_dict,

        "plan": current_plan,

        "tasks": task_state,

        "status": "DEBUGGER_DONE",
    }