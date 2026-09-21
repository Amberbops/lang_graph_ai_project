from typing import Any, Dict, List, Optional, TypedDict

from agents_v2.nodes.router import Intent


class AgentState(TypedDict, total=False):
    # ============================================================
    # Conversation
    # ============================================================

    messages: List[Any]

    # ============================================================
    # Request
    # ============================================================

    user_request: str
    intent: Intent

    # ============================================================
    # Project
    # ============================================================

    project_id: Optional[str]
    project_path: str
    project_structure: str

    # ============================================================
    # Architecture
    # ============================================================

    architecture: Optional[Dict[str, Any]]

    # ============================================================
    # Planning
    # ============================================================

    plan: Optional[Dict[str, Any]]
    tasks: List[Dict[str, Any]]

    # ============================================================
    # Debugging
    # ============================================================

    debug_analysis: Optional[Dict[str, Any]]

    # ============================================================
    # Execution
    # ============================================================

    current_task: Optional[Dict[str, Any]]
    files_changed: List[str]
    tool_calls_count: int

    # ============================================================
    # Validation
    # ============================================================

    test_results: Optional[Dict[str, Any]]
    errors: List[str]

    # ============================================================
    # Control
    # ============================================================

    status: str

    # Coder loop counter
    iteration: int

    # Debugger → Coder retry counter
    debug_iteration: int