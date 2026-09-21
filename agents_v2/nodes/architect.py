"""
Architect Node — DevPilot agents_v2.

Responsibility:
    Given the user request, detected intent, and project inspection,
    produce a high-level software architecture:

    - Chosen technology stack
    - Top-level directory / module layout
    - Key components and their responsibilities
    - Data flow between components

The architect runs AFTER the inspector and BEFORE the planner so
that the planner can break work into tasks consistent with the
intended architecture.
"""

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents_v2.models import get_reasoning_model
from agents_v2.states import AgentState


# ------------------------------------------------------------------
# Pydantic schema
# ------------------------------------------------------------------

class Component(BaseModel):
    """A top-level component in the designed architecture."""

    name: str = Field(description="Short component name (e.g. 'API Layer').")
    responsibility: str = Field(
        description="What this component does in one or two sentences."
    )
    files: List[str] = Field(
        default_factory=list,
        description="Likely files or directories that belong to this component.",
    )


class Architecture(BaseModel):
    """High-level architecture produced by the Architect agent."""

    summary: str = Field(
        description="One paragraph describing the overall design."
    )
    tech_stack: List[str] = Field(
        description="Concrete technologies, frameworks, and libraries to be used."
    )
    directory_layout: str = Field(
        description=(
            "Proposed top-level directory / file layout shown as a tree "
            "(plain text - no code fences)."
        )
    )
    components: List[Component] = Field(
        description="Key components and their responsibilities."
    )
    data_flow: str = Field(
        description=(
            "Brief prose description of how data moves through the system."
        )
    )
    constraints: List[str] = Field(
        default_factory=list,
        description=(
            "Hard constraints the implementation MUST respect "
            "(e.g. 'must not break existing auth flow')."
        ),
    )


# ------------------------------------------------------------------
# Prompt
# ------------------------------------------------------------------

architect_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Architect Agent for DevPilot, an AI software development
assistant.

Your role is to design the high-level software architecture for the
user's request BEFORE any code is written.

You will receive:
  1. The user's request
  2. The detected development intent (CREATE / MODIFY / DEBUG / ...)
  3. A summary of the existing project (if any)

Rules:
  - Choose the simplest architecture that satisfies the request.
  - Respect the existing tech stack for MODIFY / DEBUG / TEST intents.
  - For CREATE intents:
    * For web applications/tools/calculators/games/dashboards, design STANDALONE ZERO-BUILD web applications: index.html, style.css, and app.js (using CDN links for Tailwind, fonts, or icons if needed).
    * Do NOT specify Vite, Webpack, tsconfig, or npm build setups unless the user explicitly requested "React", "Next.js", "Vite", or "TypeScript". Standalone web files can be opened and run immediately in any browser without npm install.
  - Do NOT write implementation code -- only design the architecture.
  - Do NOT reference files that don't exist in the project inspection
    unless you are explicitly proposing to create them.
  - Be specific: name real frameworks and libraries, not generic terms.
  - Keep the directory layout realistic, minimal, and directly usable.

Your output is a structured architecture handed to the Planner Agent
to produce concrete implementation tasks.
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
""",
        ),
    ]
)


# ------------------------------------------------------------------
# Node function
# ------------------------------------------------------------------

def architect_node(state: AgentState) -> AgentState:
    """
    Generate a high-level architecture for the user's request.

    Runs after the inspector and before the planner.
    """

    user_request = state.get("user_request", "")
    intent = state.get("intent", "CHAT")
    project_structure = state.get(
        "project_structure",
        "No project inspection available.",
    )

    model = get_reasoning_model()

    structured_model = model.with_structured_output(Architecture)

    chain = architect_prompt | structured_model

    architecture: Architecture = chain.invoke(
        {
            "user_request": user_request,
            "intent": intent,
            "project_structure": project_structure,
        }
    )

    return {
        **state,
        "architecture": architecture.model_dump(),
        "status": "ARCHITECTED",
    }
