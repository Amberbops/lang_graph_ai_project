from typing import List, Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents_v2.models import get_reasoning_model
from agents_v2.states import AgentState


Priority = Literal[
    "CRITICAL",
    "HIGH",
    "NORMAL",
    "LOW",
]


class Task(BaseModel):
    """A single implementation task."""

    id: int = Field(
        description="Sequential task number starting from 1."
    )

    title: str = Field(
        description="Short, clear name for the task."
    )

    description: str = Field(
        description="Clear and executable description of what must be implemented."
    )

    files: List[str] = Field(
        default_factory=list,
        description=(
            "Existing or new files likely to be created or "
            "modified for this task."
        ),
    )

    priority: Priority = Field(
        description=(
            "Task priority. CRITICAL and HIGH tasks implement "
            "the core requested functionality."
        ),
    )

    required: bool = Field(
        description=(
            "Whether this task is required for the user's "
            "request to be considered implemented."
        ),
    )

    depends_on: List[int] = Field(
        default_factory=list,
        description=(
            "IDs of tasks that must be completed before this task."
        ),
    )

    reasoning: str = Field(
        default="",
        description="Short 1-sentence reason why this task is necessary."
    )



class ImplementationPlan(BaseModel):
    """Structured implementation plan produced by the Planner."""

    goal: str = Field(
        description="Overall goal of the requested change."
    )

    approach: str = Field(
        description="High-level implementation strategy."
    )

    tasks: List[Task] = Field(
        description="Ordered list of executable implementation tasks."
    )

    constraints: List[str] = Field(
        default_factory=list,
        description=(
            "Important constraints, compatibility requirements, "
            "and existing behavior that must be preserved."
        ),
    )


planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Planning Agent for DevPilot, an AI software
development agent.

Your job is to transform the user's request, project inspection,
and Architect's design into a precise, ordered implementation plan.

============================================================
INPUTS
============================================================

You will receive:

1. USER REQUEST
2. INTENT
3. PROJECT INSPECTION
4. ARCHITECTURE

============================================================
CORE PRINCIPLE
============================================================

IMPLEMENTATION FIRST.

The requested functionality is always more important than:

- README changes
- .gitignore
- documentation
- comments
- cosmetic cleanup
- optional refactoring
- optional enhancements

A working implementation must be completed before low-priority
polish.

============================================================
PRIORITIES
============================================================

CRITICAL:
Core functionality directly required by the request.

HIGH:
Supporting implementation required for the feature to work correctly.

NORMAL:
Useful supporting work that is not essential to the core request.

LOW:
Documentation, cleanup, cosmetic improvements, optional polish.

============================================================
MANDATORY RULES
============================================================

1. CRITICAL and HIGH tasks must appear before NORMAL and LOW tasks.

2. Core functionality must be marked required=true.

3. README, documentation, .gitignore, and cosmetic cleanup should
   normally be LOW priority.

4. Do not spend early tasks on low-priority work while CRITICAL
   or HIGH work remains incomplete.

5. Respect the actual project technology and structure.

6. Respect the Architect's decisions.

7. Prefer modifying existing files rather than unnecessarily
   creating new ones.

8. Do not invent project files that are not supported by the
   inspection or architecture.

9. For CREATE requests, plan the minimum complete application
   required by the user.

10. For MODIFY requests, preserve existing functionality.

11. For DEBUG requests, focus on reproducing, locating, and fixing
    the reported problem.

12. For TEST requests, focus on validation rather than unnecessary
    feature work.

13. Every task must be understandable and executable by a Coding Agent.

14. Use depends_on when task order matters.

15. Do not write implementation code.

16. Do not claim that anything has already been implemented.

17. STRICT TASK LIMIT: Produce between 4 and 7 concise, actionable tasks. NEVER generate more than 8 tasks. Consolidate related subcomponents into cohesive tasks so the plan remains compact and executive.

18. CORE APPLICATION FIRST: Task 1 MUST always be the primary working application code (e.g. index.html, style.css, app.js, or main application logic). NEVER make package.json, tsconfig.json, or build configs Task 1. Users must get a functional, runnable application even if execution concludes early.

============================================================
COMPLETION CRITERIA
============================================================

The plan is complete only when the user's requested functionality
can be considered implemented and testable.

For CREATE:
- Build the actual application.
- Implement the core UI or API.
- Implement core behavior.
- Add required supporting files.
- Validate the result.
- Documentation comes later.

For MODIFY:
- Understand the existing implementation.
- Change only what is necessary.
- Preserve unrelated behavior.
- Validate the modification.

For DEBUG:
- Identify the likely failure area.
- Define the fix.
- Include validation of the fix.

============================================================
OUTPUT
============================================================

Return only the structured implementation plan.
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

ARCHITECTURE:
{architecture}
""",
        ),
    ]
)


def planner_node(state: AgentState) -> AgentState:
    """
    Create a structured implementation plan from:

    - user request
    - detected intent
    - project inspection
    - Architect output
    """

    user_request = state.get(
        "user_request",
        "",
    )

    intent = state.get(
        "intent",
        "CHAT",
    )

    project_structure = state.get(
        "project_structure",
        "No project inspection available.",
    )

    architecture = state.get(
        "architecture"
    ) or {}

    # --------------------------------------------------------------
    # Convert Architect result into readable prompt text
    # --------------------------------------------------------------

    if architecture:

        tech_stack = architecture.get(
            "tech_stack",
            [],
        )

        constraints = architecture.get(
            "constraints",
            [],
        )

        arch_text = (
            f"Summary: "
            f"{architecture.get('summary', '')}\n\n"
            f"Tech stack: "
            f"{', '.join(tech_stack)}\n\n"
            f"Directory layout:\n"
            f"{architecture.get('directory_layout', '')}\n\n"
            f"Data flow:\n"
            f"{architecture.get('data_flow', '')}\n\n"
            f"Constraints: "
            f"{'; '.join(constraints)}"
        )

    else:
        arch_text = (
            "No architecture document is available. "
            "Use the project inspection and request."
        )

    # --------------------------------------------------------------
    # Reasoning model
    # --------------------------------------------------------------

    model = get_reasoning_model()

    structured_model = model.with_structured_output(
        ImplementationPlan
    )

    chain = planner_prompt | structured_model

    try:
        plan = chain.invoke(
            {
                "user_request": user_request,
                "intent": intent,
                "project_structure": project_structure,
                "architecture": arch_text,
            }
        )
    except Exception as exc:
        print(f"Warning: Primary planner output failed ({exc}). Using resilient fallback plan.")
        plan = ImplementationPlan(
            goal=f"Build and complete the requested project: {user_request[:100]}",
            approach="Implement core application files, styling, and interactive behavior based on architecture.",
            tasks=[
                Task(
                    id=1,
                    title="Implement core application files and structure",
                    description="Write the main application files (HTML, markup, and root components).",
                    files=["index.html"],
                    priority="CRITICAL",
                    required=True,
                    reasoning="Scaffolding and foundational structure.",
                ),
                Task(
                    id=2,
                    title="Implement styling and visual theme",
                    description="Implement CSS styling, themes, layout, and visual components.",
                    files=["style.css"],
                    priority="HIGH",
                    required=True,
                    reasoning="Visual presentation and styling.",
                ),
                Task(
                    id=3,
                    title="Implement application logic and interactivity",
                    description="Write script logic, state management, event listeners, and user interaction.",
                    files=["script.js"],
                    priority="CRITICAL",
                    required=True,
                    reasoning="Core interactive functionality.",
                ),
                Task(
                    id=4,
                    title="Verify functionality and document project",
                    description="Test application behavior, fix any edge cases, and provide documentation.",
                    files=["README.md"],
                    priority="NORMAL",
                    required=False,
                    reasoning="Verification and project documentation.",
                ),
            ],
            constraints=[],
        )

    # --------------------------------------------------------------
    # Convert structured plan into AgentState
    # --------------------------------------------------------------

    plan_dict = plan.model_dump()

    task_dicts = [
        task.model_dump()
        for task in plan.tasks
    ]


    return {
        **state,
        "plan": plan_dict,
        "tasks": task_dicts,
        "status": "PLANNED",
    }