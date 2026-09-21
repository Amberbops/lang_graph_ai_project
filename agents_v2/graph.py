"""
DevPilot Agentic Graph — agents_v2.

Current architecture:

    START
      │
      ▼
    ROUTER
      │
      ├── CHAT ─────────────────────────────► END
      │
      ▼
    INSPECTOR
      │
      ├── EXPLAIN ───────► EXPLAINER ───────► END
      │
      ├── TEST ──────────► TESTER
      │
      ├── DEBUG ─────────► DEBUGGER
      │
      └── CREATE / MODIFY
                │
                ▼
             ARCHITECT
                │
                ▼
              PLANNER
                │
                ▼
              CODER
                │
                ├── TOOL_EXECUTION ───► CODER
                │
                ▼
              TESTER
                │
          ┌─────┴─────┐
          │           │
         PASS        FAIL
          │           │
          ▼           ▼
         END       DEBUGGER
                      │
                      ▼
                 CODER_RETRY
                      │
                      ▼
                    CODER
                      │
                      ▼
                    TESTER
"""

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from agents_v2.models import get_fast_model
from agents_v2.states import AgentState

from agents_v2.nodes.router import route_request
from agents_v2.nodes.inspector import inspector_node
from agents_v2.nodes.architect import architect_node
from agents_v2.nodes.planner import planner_node
from agents_v2.nodes.coder import coder_node
from agents_v2.nodes.debugger import debugger_node
from agents_v2.nodes.tester import tester_node


# ------------------------------------------------------------------
# Maximum number of Debugger → Coder retry cycles.
# ------------------------------------------------------------------

MAX_DEBUG_CYCLES = 3


# ==================================================================
# ROUTER NODE
# ==================================================================

def router_node(
    state: AgentState,
) -> AgentState:
    """Classify the user's request."""

    user_request = state.get(
        "user_request",
        "",
    )

    intent = route_request(
        user_request
    )

    return {
        **state,
        "intent": intent,
        "status": "ROUTED",
    }


# ==================================================================
# EXPLAINER NODE
# ==================================================================

def explainer_node(
    state: AgentState,
) -> AgentState:
    """
    Explain project-related questions without modifying files.
    """

    user_request = state.get(
        "user_request",
        "",
    )

    project_structure = state.get(
        "project_structure",
        "No project inspection available.",
    )

    model = get_fast_model()

    response = model.invoke(
        f"""
You are DevPilot's Explainer Agent.

The user has requested an explanation.

Use the project context below and provide a clear,
accurate answer.

USER REQUEST:
{user_request}

PROJECT CONTEXT:
{project_structure}

Rules:

- Be accurate and concise.
- Reference actual project information when relevant.
- Do not invent files or implementation details.
- Do not modify any files.
- Do not claim code was run unless the context proves it.
"""
    )

    explanation = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    return {
        **state,

        "messages": [
            *state.get(
                "messages",
                []
            ),
            HumanMessage(
                content=user_request
            ),
            response,
        ],

        "status": "EXPLAINED",

        "plan": {
            "goal": "Explain",
            "approach": explanation,
            "tasks": [],
            "constraints": [],
        },
    }


# ==================================================================
# ROUTING AFTER ROUTER
# ==================================================================

def route_after_router(
    state: AgentState,
) -> str:
    """
    Decide whether project inspection is required.
    """

    intent = state.get(
        "intent"
    )

    if intent in {
        "CREATE",
        "MODIFY",
        "DEBUG",
        "TEST",
        "EXPLAIN",
    }:
        return "inspector"

    return "end"


# ==================================================================
# ROUTING AFTER INSPECTOR
# ==================================================================

def route_after_inspector(
    state: AgentState,
) -> str:
    """
    Route the request to the correct specialist.
    """

    intent = state.get(
        "intent"
    )

    if intent == "EXPLAIN":
        return "explainer"

    if intent == "DEBUG":
        return "debugger"

    if intent == "TEST":
        return "tester"

    # CREATE / MODIFY
    return "architect"


# ==================================================================
# ROUTING AFTER CODER
# ==================================================================

def route_after_coder(
    state: AgentState,
) -> str:
    """
    Decide whether the Coder continues, validates,
    or terminates because of failure.
    """

    status = state.get(
        "status",
        "",
    )

    if status == "TOOL_EXECUTION":
        return "coder"

    if status == "CODER_DONE":
        return "tester"

    if status in {
        "CODER_FAILED",
        "CODER_LIMIT_REACHED",
        "CODER_TOOL_FAILURE",
    }:
        return "end"

    return "end"


# ==================================================================
# ROUTING AFTER TESTER
# ==================================================================

def route_after_tester(
    state: AgentState,
) -> str:
    """
    Decide whether validation passed or debugging is required.
    """

    status = state.get(
        "status",
        "",
    )

    debug_iteration = state.get(
        "debug_iteration",
        0,
    )

    # --------------------------------------------------------------
    # Actual automated tests passed.
    # --------------------------------------------------------------

    if status == "TESTS_PASSED":
        return "end"

    # --------------------------------------------------------------
    # Build or static validation passed.
    # --------------------------------------------------------------

    if status == "VALIDATION_PASSED":
        return "end"

    # --------------------------------------------------------------
    # No tests are available.
    # Do not create a pointless debug loop.
    # --------------------------------------------------------------

    if status == "NO_TESTS":
        return "end"

    # --------------------------------------------------------------
    # Maximum debug cycles reached.
    # --------------------------------------------------------------

    if debug_iteration >= MAX_DEBUG_CYCLES:
        return "end"

    # --------------------------------------------------------------
    # Failed test or validation execution.
    # --------------------------------------------------------------

    if status in {
        "TESTS_FAILED",
        "TEST_ERROR",
        "VALIDATION_FAILED",
    }:
        return "debugger"

    return "end"


# ==================================================================
# ROUTING AFTER DEBUGGER
# ==================================================================

def route_after_debugger(
    state: AgentState,
) -> str:
    """
    Decide whether the diagnosis is suitable for a Coder retry.
    """

    status = state.get(
        "status",
        "",
    )

    if status == "DEBUGGER_FAILED":
        return "end"

    if status == "DEBUGGER_LIMIT_REACHED":
        return "end"

    if status == "DEBUGGER_DONE":
        return "coder_retry"

    return "end"


# ==================================================================
# CODER RETRY RESET
# ==================================================================

def coder_retry_node(
    state: AgentState,
) -> AgentState:
    """
    Prepare a fresh Coder pass after debugging.

    The actual project files remain untouched here.

    We reset only the Coder's temporary conversation and
    iteration counter.
    """

    debug_iteration = state.get(
        "debug_iteration",
        0,
    )

    return {
        **state,

        # Start a new Coder reasoning session.
        "messages": [],

        # Reset Coder iteration budget.
        "iteration": 0,

        # Increment Debugger retry cycle.
        "debug_iteration": (
            debug_iteration + 1
        ),

        "status": "RETRY_CODER",
    }


# ==================================================================
# GRAPH BUILDER
# ==================================================================

def build_graph():

    graph = StateGraph(
        AgentState
    )

    # --------------------------------------------------------------
    # Nodes
    # --------------------------------------------------------------

    graph.add_node(
        "router",
        router_node,
    )

    graph.add_node(
        "inspector",
        inspector_node,
    )

    graph.add_node(
        "explainer",
        explainer_node,
    )

    graph.add_node(
        "architect",
        architect_node,
    )

    graph.add_node(
        "planner",
        planner_node,
    )

    graph.add_node(
        "coder",
        coder_node,
    )

    graph.add_node(
        "tester",
        tester_node,
    )

    graph.add_node(
        "debugger",
        debugger_node,
    )

    graph.add_node(
        "coder_retry",
        coder_retry_node,
    )

    # --------------------------------------------------------------
    # START → ROUTER
    # --------------------------------------------------------------

    graph.add_edge(
        START,
        "router",
    )

    # --------------------------------------------------------------
    # ROUTER → INSPECTOR / END
    # --------------------------------------------------------------

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "inspector": "inspector",
            "end": END,
        },
    )

    # --------------------------------------------------------------
    # INSPECTOR → specialist
    # --------------------------------------------------------------

    graph.add_conditional_edges(
        "inspector",
        route_after_inspector,
        {
            "explainer": "explainer",
            "debugger": "debugger",
            "tester": "tester",
            "architect": "architect",
        },
    )

    # --------------------------------------------------------------
    # EXPLAINER → END
    # --------------------------------------------------------------

    graph.add_edge(
        "explainer",
        END,
    )

    # --------------------------------------------------------------
    # ARCHITECT → PLANNER → CODER
    # --------------------------------------------------------------

    graph.add_edge(
        "architect",
        "planner",
    )

    graph.add_edge(
        "planner",
        "coder",
    )

    # --------------------------------------------------------------
    # CODER → CODER / TESTER / END
    # --------------------------------------------------------------

    graph.add_conditional_edges(
        "coder",
        route_after_coder,
        {
            "coder": "coder",
            "tester": "tester",
            "end": END,
        },
    )

    # --------------------------------------------------------------
    # TESTER → END / DEBUGGER
    # --------------------------------------------------------------

    graph.add_conditional_edges(
        "tester",
        route_after_tester,
        {
            "end": END,
            "debugger": "debugger",
        },
    )

    # --------------------------------------------------------------
    # DEBUGGER → CODER_RETRY / END
    # --------------------------------------------------------------

    graph.add_conditional_edges(
        "debugger",
        route_after_debugger,
        {
            "coder_retry": "coder_retry",
            "end": END,
        },
    )

    # --------------------------------------------------------------
    # CODER_RETRY → CODER
    # --------------------------------------------------------------

    graph.add_edge(
        "coder_retry",
        "coder",
    )

    return graph.compile()


# ==================================================================
# COMPILED APPLICATION
# ==================================================================

app = build_graph()