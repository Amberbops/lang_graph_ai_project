import time

from dotenv import load_dotenv
from langchain_core.globals import set_verbose, set_debug
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain.agents import create_agent
from groq import RateLimitError, BadRequestError
from agent.tools import init_project_root
from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files

_ = load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")


def invoke_with_retry(runnable, *args, max_retries=5, base_wait=10, **kwargs):
    """Invoke a runnable, retrying on Groq rate-limit (429) and tool-call-parsing (400) errors."""
    for attempt in range(max_retries):
        try:
            return runnable.invoke(*args, **kwargs)
        except RateLimitError as e:
            wait = base_wait * (attempt + 1)
            print(f"Rate limit hit (attempt {attempt + 1}/{max_retries}), retrying in {wait}s...")
            time.sleep(wait)
        except BadRequestError as e:
            if "tool_use_failed" in str(e):
                print(f"Tool call JSON parse failed (attempt {attempt + 1}/{max_retries}), retrying...")
                time.sleep(2)
            else:
                raise
    # final attempt, let any error surface naturally
    return runnable.invoke(*args, **kwargs)


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    resp = invoke_with_retry(
        llm.with_structured_output(Plan),
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]

    resp = invoke_with_retry(
        llm.with_structured_output(TaskPlan),
        architect_prompt(plan=plan.model_dump_json())
    )

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    return {
        "task_plan": resp,
        "plan": plan
    }

def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    MAX_CHARS = 4000

    existing_content = read_file.run(current_task.filepath)

    if len(existing_content) > MAX_CHARS:
        existing_content = existing_content[:MAX_CHARS]

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_agent(llm, coder_tools)
    print("TASK LENGTH:", len(current_task.task_description))
    print("FILE LENGTH:", len(existing_content))
    invoke_with_retry(
        react_agent,
        {"messages": [{"role": "system", "content": system_prompt},
                       {"role": "user", "content": user_prompt}]}
    )

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}

init_project_root()

graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()
if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)