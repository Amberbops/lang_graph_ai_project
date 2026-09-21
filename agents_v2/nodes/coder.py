from langchain_core.messages import HumanMessage

from agents_v2.models import get_coding_model, invoke_with_retry
from agents_v2.states import AgentState


from tools.filesystem.operations import (
    read_file,
    write_file,
    list_files,
    delete_file,
    clear_workspace,
)

from tools.terminal.executor import run_cmd
from tools.testing.testing import run_tests

from agents_v2.nodes.tool_executor import (
    execute_tool_calls,
)


MAX_CODER_ITERATIONS = 12


CODER_TOOLS = [
    read_file,
    write_file,
    list_files,
    delete_file,
    clear_workspace,
    run_cmd,
    run_tests,
]



def coder_node(state: AgentState) -> AgentState:
    """
    Coding Agent.

    Uses Gemini/Groq tool calling to inspect and modify the project.
    """

    # ==============================================================
    # STATE
    # ==============================================================

    iteration = state.get(
        "iteration",
        0,
    )

    user_request = state.get(
        "user_request",
        "",
    )

    intent = state.get(
        "intent",
        "MODIFY",
    )

    project_structure = state.get(
        "project_structure",
        "No project inspection available.",
    )

    plan = state.get(
        "plan",
        {},
    )

    tasks = state.get(
        "tasks",
        [],
    )

    messages = state.get(
        "messages",
        [],
    )

    files_changed = state.get(
        "files_changed",
        [],
    )

    # ==============================================================
    # HARD ITERATION LIMIT
    # ==============================================================

    if iteration >= MAX_CODER_ITERATIONS:

        return {
            **state,

            "status": "CODER_LIMIT_REACHED",

            "errors": [
                *state.get("errors", []),
                (
                    "Coder stopped after reaching the maximum "
                    f"iteration limit of "
                    f"{MAX_CODER_ITERATIONS}."
                ),
            ],
        }

    # ==============================================================
    # MODEL + TOOLS
    # ==============================================================

    model = get_coding_model().bind_tools(
        CODER_TOOLS,
        tool_choice="auto",
    )

    # ==============================================================
    # INITIAL CODER PROMPT
    # ==============================================================

    if not messages:

        coder_prompt = f"""
You are DevPilot's Coding Agent.

Your job is to ACTUALLY implement the user's request inside
the project workspace.

============================================================
USER REQUEST
============================================================

{user_request}

============================================================
INTENT
============================================================

{intent}

============================================================
PROJECT INSPECTION
============================================================

{project_structure}

============================================================
IMPLEMENTATION PLAN
============================================================

{plan}

============================================================
TASKS
============================================================

{tasks}

============================================================
TASK EXECUTION PRIORITY
============================================================

Execute tasks in this order:

1. CRITICAL
2. HIGH
3. NORMAL
4. LOW

Never spend an early iteration on README, documentation,
.gitignore, comments, or cosmetic cleanup while CRITICAL
or HIGH implementation tasks remain unfinished.

============================================================
MANDATORY RULES
============================================================

1. Work only inside the project workspace.

2. Inspect existing files before modifying them.

3. Use tools for actual project operations.

4. Do not fabricate file contents.

5. Do not fabricate tool results.

6. Do not claim a file changed unless write_file actually
   changed it.

7. Prefer modifying existing files where appropriate.

8. Preserve existing functionality unless the user explicitly
   requested otherwise.

9. Implement core functionality before documentation or polish.

10. Use run_cmd when execution or validation is useful.

11. Use run_tests when tests are available and relevant.

12. Continue implementing CRITICAL and HIGH tasks before
   low-priority tasks.

13. Do not merely tell the user what code they should write.
   Perform the work using the tools.

14. For CREATE or MODIFY requests, the implementation normally
   requires write_file.

15. If a tool result reveals an error, use that information
   to correct the implementation.

16. MANDATORY COMPLETE APPLICATION FILES: For any web app, tool, or UI, you MUST generate complete, working application files: `index.html`, `style.css`, and `app.js`. Every generated web project MUST have a fully functional `index.html` that can be opened and used directly in any browser.

17. NEVER STOP AT CONFIG FILES: Do NOT generate only `package.json`, `tsconfig.json`, or `vite.config.ts`. If any config file is created, you MUST ALSO create `index.html`, `style.css`, and `app.js` with all functional logic, styling, and interactive UI. Stopping with only config files is considered a critical failure.

18. BATCH GENERATION RULE: To prevent API rate limits and maximize efficiency, call `write_file` for all required files (`index.html`, `style.css`, `app.js`, etc.) together in parallel tool calls in your very first turn.

19. If the user request asks to clear or recreate the workspace from scratch, call clear_workspace alongside write_file.

20. Write all essential application code files (HTML, CSS, JS, backend logic) before any README or documentation.

21. Once all working files are created, conclude in the subsequent turn with a concise confirmation summary and no more tool calls.

============================================================
AVAILABLE TOOLS
============================================================

read_file
write_file
list_files
delete_file
clear_workspace
run_cmd
run_tests

Begin by writing all core project files (index.html, style.css, app.js) using write_file.
"""


        messages = [
            HumanMessage(
                content=coder_prompt
            )
        ]

    # ==============================================================
    # ASK MODEL FOR NEXT ACTION (with sliding window & retry)
    # ==============================================================

    # Sliding window: keep root instructions (messages[0]) + last 4 turns
    # This keeps token footprint around ~1500 tokens, well below 8000 TPM limit!
    pruned_messages = messages
    if len(messages) > 5:
        pruned_messages = [messages[0], *messages[-4:]]

    response = invoke_with_retry(
        model,
        pruned_messages,
    )


    # ==============================================================
    # TOOL CALLS
    # ==============================================================

    if response.tool_calls:

        tool_messages, changed_files = execute_tool_calls(
            response
        )

        updated_messages = [
            *messages,
            response,
            *tool_messages,
        ]

        # Keep file list unique while preserving order.
        updated_files_changed = list(
            dict.fromkeys(
                [
                    *files_changed,
                    *changed_files,
                ]
            )
        )

        return {
            **state,

            "messages": updated_messages,

            "status": "TOOL_EXECUTION",

            "iteration": iteration + 1,

            "files_changed": updated_files_changed,

            "tool_calls_count": (
                state.get(
                    "tool_calls_count",
                    0,
                )
                + len(response.tool_calls)
            ),

            "current_task": {
                "tool_calls": response.tool_calls,
            },
        }

    # ==============================================================
    # NO TOOL CALL
    # ==============================================================

    updated_messages = [
        *messages,
        response,
    ]

    # --------------------------------------------------------------
    # Actual implementation happened
    # --------------------------------------------------------------

    if files_changed:

        return {
            **state,

            "messages": updated_messages,

            "status": "CODER_DONE",

            "iteration": iteration + 1,

            "current_task": {
                "response": response.content,
            },
        }

    # --------------------------------------------------------------
    # Model stopped without modifying anything
    # --------------------------------------------------------------

    return {
        **state,

        "messages": updated_messages,

        "status": "CODER_FAILED",

        "iteration": iteration + 1,

        "errors": [
            *state.get("errors", []),
            (
                "Coder stopped without modifying any files."
            ),
        ],

        "current_task": {
            "response": response.content,
        },
    }