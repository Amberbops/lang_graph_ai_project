# LangGraph AI Code Generation Agent

A multi-agent pipeline built with LangGraph that converts a plain-English project prompt into a fully implemented codebase. Three specialized agents — **Planner**, **Architect**, and **Coder** — collaborate in sequence, each handling a distinct phase of software engineering.

---

## How It Works

```
User Prompt → Planner → Architect → Coder (loop) → Generated Project
```

### Agents

| Agent | Responsibility |
|---|---|
| **Planner** | Converts the user prompt into a structured project plan (name, description, tech stack, features, files) |
| **Architect** | Breaks the plan into ordered, self-contained implementation tasks, one or more per file |
| **Coder** | Executes each task using a ReAct loop with file-system tools, writing the actual code |

The Coder runs in a loop — one iteration per implementation task — until all tasks are complete.

---

## Project Structure

```
lang_graph_ai_project/
├── agent/
│   ├── __init__.py          # Package exports
│   ├── graph.py             # LangGraph pipeline: nodes, edges, retry logic
│   ├── prompts.py           # Prompt templates for each agent
│   ├── states.py            # Pydantic models: Plan, TaskPlan, CoderState
│   └── tools.py             # File-system tools: read_file, write_file, list_files
├── generated_project/       # Output directory — all generated files land here
├── main.py                  # CLI entry point
└── .env                     # API keys (not committed)
```

---

## Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com/) (free tier supported; Dev tier recommended for larger projects)
- [`uv`](https://github.com/astral-sh/uv) or `pip` for package management

---

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd lang_graph_ai_project

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install langchain langchain-groq langgraph pydantic python-dotenv
```

---

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The pipeline uses the `openai/gpt-oss-120b` model via Groq. No other API keys are required.

---

## Usage

### Run via CLI (recommended)

```bash
python main.py
```

You will be prompted to enter your project description:

```
Enter your project prompt: Build a colourful modern todo app in html css and js
```

### Run directly

```bash
python agent/graph.py
```

This runs with a hardcoded prompt defined at the bottom of `graph.py`.

### Optional flags

```bash
python main.py --recursion-limit 200   # Increase limit for larger projects (default: 100)
```

### Output

All generated files are written to `generated_project/` in the project root. For a typical web app this will contain `index.html`, `styles.css`, `app.js`, `README.md`, and so on.

---

## Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Graph-based multi-agent orchestration |
| `langchain` | Agent creation (`create_agent`), prompt utilities |
| `langchain-groq` | Groq LLM integration (`ChatGroq`) |
| `langchain-core` | Base runnables, globals (`set_debug`, `set_verbose`) |
| `pydantic` | State models (`Plan`, `TaskPlan`, `CoderState`) |
| `python-dotenv` | `.env` file loading |
| `groq` | Direct Groq client for error handling |

---

## Known Limitations & Tips

**Rate limits on free tier**
Groq's free tier is capped at 8,000 tokens per minute. The pipeline includes automatic retry with exponential backoff for `429 RateLimitError`. Large projects with many implementation steps will take longer due to enforced waits between requests. Upgrading to the [Dev tier](https://console.groq.com/settings/billing) removes this bottleneck.

**Large file generation**
Writing large files (e.g. a complex `app.js`) in a single tool call can occasionally cause Groq to return a `400 tool_use_failed` error due to JSON escaping issues with deeply nested quotes. The pipeline retries these automatically. If retries consistently fail, consider prompting for smaller, more focused tasks.

**Recursion limit**
Each Coder iteration counts against LangGraph's recursion limit. For projects with many files or tasks, pass a higher `--recursion-limit` value. The default is 100.

**`generated_project/` is overwritten**
Re-running the pipeline with the same prompt will overwrite previously generated files. Back up the output folder if you want to preserve prior runs.

---

## Architecture Notes

### State flow

```python
# AgentState (dict) passed between nodes:
{
  "user_prompt": str,
  "plan": Plan,
  "task_plan": TaskPlan,
  "coder_state": CoderState,   # tracks current_step_idx
  "status": str                # "DONE" signals loop exit
}
```

### Retry logic

`invoke_with_retry()` in `graph.py` wraps all three agent `.invoke()` calls:

- **`RateLimitError` (429)** — retries up to 5 times with linear backoff (10s, 20s, 30s, ...)
- **`BadRequestError` with `tool_use_failed` (400)** — retries up to 5 times with a short 2s delay

### Tools available to the Coder

| Tool | Description |
|---|---|
| `read_file(path)` | Read a file from `generated_project/` |
| `write_file(path, content)` | Write or overwrite a file in `generated_project/` |
| `list_files(directory)` | List files in `generated_project/` |
| `get_current_directory()` | Return the absolute path of `generated_project/` |

All paths are sandboxed — attempts to write outside `generated_project/` raise a `ValueError`.

---

## Example Run

```
$ python main.py
Enter your project prompt: Build a colourful modern todo app in html css and js

PROJECT_ROOT = C:\...\generated_project
[chain/start] [chain:LangGraph] Entering Chain run ...
  → Planner:   ColorfulTodo plan created (4 files, 8 features)
  → Architect: 4 implementation tasks generated
  → Coder [1/4]: index.html written
  → Coder [2/4]: styles.css written
  → Coder [3/4]: app.js written
  → Coder [4/4]: README.md written
Final State: { "status": "DONE", ... }
```

---

## License

MIT — feel free to use and extend.
