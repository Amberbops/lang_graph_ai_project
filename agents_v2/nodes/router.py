from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents_v2.models import get_router_model


Intent = Literal[
    "CREATE",
    "MODIFY",
    "DEBUG",
    "TEST",
    "EXPLAIN",
    "CHAT",
]


class RouterDecision(BaseModel):
    """Structured result returned by the intent router."""

    intent: Intent = Field(
        description=(
            "The single software-development intent that best "
            "matches the user's request."
        )
    )


router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the intent router for DevPilot,
an AI software development agent.

Classify the user's request into exactly ONE intent.

CREATE:
The user wants to build a new application, website,
API, script, or software project.

MODIFY:
The user wants to change, add, remove, improve,
refactor, or extend an existing project.

DEBUG:
The user reports a bug, crash, exception, error,
or unexpected behavior and wants it investigated or fixed.

TEST:
The user wants to run, create, inspect, or validate tests.

EXPLAIN:
The user wants an explanation of code, architecture,
implementation, errors, or software concepts in relation
to their project.

CHAT:
The request is ordinary conversation and does not require
project development work.

Examples:

"Build me a todo app" -> CREATE
"Create a REST API for a blog" -> CREATE

"Add dark mode to my React app" -> MODIFY
"Change the navbar color" -> MODIFY

"My login button crashes" -> DEBUG
"Why am I getting this TypeScript error?" -> DEBUG

"Run the tests" -> TEST
"Check whether my application works" -> TEST

"Explain this authentication code" -> EXPLAIN
"What does this function do?" -> EXPLAIN

"Hello" -> CHAT
"How are you?" -> CHAT
""",
        ),
        (
            "human",
            "{user_request}",
        ),
    ]
)


def route_request(user_request: str) -> Intent:
    """
    Classify a user request using Gemini structured output.
    """

    if not user_request or not user_request.strip():
        return "CHAT"

    model = get_router_model()

    # Force Gemini to return a validated Pydantic structure.
    structured_model = model.with_structured_output(
        RouterDecision
    )

    chain = router_prompt | structured_model

    decision = chain.invoke(
        {
            "user_request": user_request.strip(),
        }
    )

    return decision.intent