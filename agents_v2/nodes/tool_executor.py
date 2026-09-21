from langchain_core.messages import ToolMessage

from tools.filesystem.operations import (
    read_file,
    write_file,
    list_files,
    delete_file,
    clear_workspace,
)

from tools.terminal.executor import run_cmd
from tools.testing.testing import run_tests


# ------------------------------------------------------------------
# Available tools for the Coding and Debugging Agents
# ------------------------------------------------------------------

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "delete_file": delete_file,
    "clear_workspace": clear_workspace,
    "run_cmd": run_cmd,
    "run_tests": run_tests,
}




def execute_tool_calls(response):
    """
    Execute all tool calls requested by Gemini.

    Args:
        response:
            AIMessage returned by the Gemini model.

    Returns:
        tuple:
            (
                list[ToolMessage],
                list[str]
            )

        The first item contains tool results.
        The second item contains files modified by write_file.
    """

    tool_messages = []
    changed_files = []

    # --------------------------------------------------------------
    # No tool calls
    # --------------------------------------------------------------

    if not getattr(response, "tool_calls", None):
        return tool_messages, changed_files

    # --------------------------------------------------------------
    # Execute every requested tool
    # --------------------------------------------------------------

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call["id"]

        # ----------------------------------------------------------
        # Validate tool
        # ----------------------------------------------------------

        tool = TOOL_MAP.get(tool_name)

        if tool is None:

            tool_messages.append(
                ToolMessage(
                    content=(
                        f"Unknown tool requested: "
                        f"{tool_name}"
                    ),
                    tool_call_id=tool_call_id,
                )
            )

            continue

        # ----------------------------------------------------------
        # Execute tool
        # ----------------------------------------------------------

        try:

            result = tool.invoke(tool_args)

            # ------------------------------------------------------
            # Track modified files
            # ------------------------------------------------------

            if tool_name == "write_file":

                path = tool_args.get("path")

                if path:
                    changed_files.append(path)

            # ------------------------------------------------------
            # Return tool result to Gemini
            # ------------------------------------------------------

            tool_messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call_id,
                )
            )

        except Exception as exc:

            # ------------------------------------------------------
            # Tool failure should become information for Gemini,
            # not crash the entire agent immediately.
            # ------------------------------------------------------

            error_message = (
                f"Tool '{tool_name}' failed.\n"
                f"Error type: {type(exc).__name__}\n"
                f"Error: {exc}"
            )

            tool_messages.append(
                ToolMessage(
                    content=error_message,
                    tool_call_id=tool_call_id,
                )
            )

    return tool_messages, changed_files