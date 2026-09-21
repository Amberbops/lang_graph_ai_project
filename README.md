# ⚡ NEON GENESIS — Autonomous AI Software Development Agent & Web Studio

> **Autonomous Agentic Pipeline & Web Studio powered by LangGraph, Groq, and Google Gemini.**  
> Transform natural language ideas into full-stack codebases and download them as production-ready `.zip` archives with real-time **Antigravity-style generating timers**.

---

## 👨‍💻 Project Owner & Maintainer

- **Owner**: Amber Saluja
- **Contact / Email**: [ambersaluja20006@gmail.com](mailto:ambersaluja20006@gmail.com)
- **Repository**: `lang_graph_ai_project` (DevPilot v2.0)

---

## 🌟 Key Highlights

- **🧠 Dual-Provider LLM Orchestration**:
  - **Gemini 3.5 Flash-Lite**: Lightning-fast intent classification (`router`), project filesystem scanning (`inspector`), and test output parsing (`tester`).
  - **Groq `openai/gpt-oss-120b` / Compound**: High-capacity reasoning, technical design (`architect`), task planning (`planner`), tool-calling code generation (`coder`), and debugging (`debugger`).
  - **Self-Healing Model Prober**: Automatically tests Groq models at startup and selects the best active model, skipping decommissioned models cleanly.
- **⚡ 7-Node LangGraph State Machine**:
  - `Router` → `Inspector` → `Architect` → `Planner` → `Coder` (tool execution loop) → `Tester` → `Packager`.
  - Self-healing debugging loop: If tests fail, the `debugger` node diagnoses the root cause and passes the fix plan back to `coder`.
- **⏱️ Antigravity-Style Live Timers**:
  - Master digital stopwatch with 60ms millisecond precision tracking total generation time.
  - Per-step milestone timers with live pulsing neon status indicators.
- **📦 Instant ZIP Export & Code Previewer**:
  - One-click `.zip` packaging of the generated workspace.
  - In-browser code preview modal with syntax formatting.
- **🌐 Zero-Dependency Web Studio**:
  - Built-in multi-threaded Python server (`web_app/server.py`) requiring zero external web framework installations.
  - Futuristic Neon Cyberpunk UI with quick template prompts and live terminal logs.

---

## 🏗️ Architecture & Agentic Chain

```
                ┌──────────────┐
                │  User Prompt │
                └──────┬───────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Router Node   │ (Gemini Flash-Lite)
              └────────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       │ (EXPLAIN)     │ (CREATE/MOD)  │ (CHAT)
       ▼               ▼               ▼
 ┌───────────┐   ┌───────────┐    ┌─────────┐
 │ Explainer │   │ Inspector │    │ Direct  │
 └─────┬─────┘   └─────┬─────┘    │ Reply   │
       │               │          └────┬────┘
       │               ▼               │
       │         ┌───────────┐         │
       │         │ Architect │ (Groq 120B)
       │         └─────┬─────┘         │
       │               │               │
       │               ▼               │
       │         ┌───────────┐         │
       │         │  Planner  │ (Groq 120B)
       │         └─────┬─────┘         │
       │               │               │
       │               ▼               │
       │         ┌───────────┐         │
       │   ┌────►│   Coder   │◄────┐   │
       │   │     └─────┬─────┘     │   │
       │   │ (Loop)    │           │   │
       │   └───────────┘           │   │
       │               ▼           │   │
       │         ┌───────────┐     │   │
       │         │  Tester   │     │   │
       │         └─────┬─────┘     │   │
       │               │           │   │
       │     (Pass) ┌──┴──┐ (Fail) │   │
       │      ┌─────┘     └─────┐  │   │
       │      ▼                 ▼  │   │
       │ ┌──────────┐     ┌────────┴─┐ │
       │ │ Packager │     │ Debugger ├─┘
       │ └────┬─────┘     └──────────┘
       │      │
       ▼      ▼
   ┌─────────────┐
   │ Output .ZIP │
   └─────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup

Clone the repository and install dependencies using `uv` or standard Python `pip`:

```powershell
cd lang_graph_ai_project

# Using uv (recommended)
uv sync

# Or using pip
python -m venv .venv
.venv\Scripts\activate
pip install -r pyproject.toml
```

### 2. Configure API Keys

Create or edit `.env` in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## 💻 Running the Application

### Option A: Web Studio (Recommended)

Launch the Neon Web Studio on port 5000:

```powershell
uv run python web_app/server.py --port 5000
```

Open your browser to:
👉 **[http://localhost:5000](http://localhost:5000)**

- **Studio (`/`)**: Input your prompt, watch the Antigravity timers tick, and download the finished project as `.zip`.
- **About Page (`/about.html`)**: Interactive system documentation, architecture overview, and creator contact.

### Option B: Terminal CLI

Run DevPilot directly in the command line:

```powershell
uv run python main.py
```

Optional CLI flags:
```powershell
uv run python main.py --clean                  # Clear generated_project workspace before running
uv run python main.py --recursion-limit 200    # Increase LangGraph step limit for huge codebases
```

---

## 📂 Project Structure

```
lang_graph_ai_project/
├── agents_v2/                 # Autonomous Agentic Engine
│   ├── graph.py               # LangGraph state machine & conditional routing
│   ├── models.py              # Dual-provider LLM router & self-healing Groq prober
│   ├── states.py              # AgentState TypedDict definitions
│   └── nodes/                 # Specialized agent nodes
│       ├── router.py          # Intent classification & routing
│       ├── inspector.py       # Filesystem structure analyzer
│       ├── architect.py       # High-level architecture designer
│       ├── planner.py         # Structured milestone planner (resilient fallback)
│       ├── coder.py           # ReAct tool-calling coding agent (25 iterations)
│       ├── debugger.py        # Automated bug diagnosis & root-cause analyzer
│       ├── tester.py          # Automated test execution & verification
│       └── tool_executor.py   # Tool dispatch and execution tracking
├── tools/                     # Agent Tools
│   ├── filesystem/            # read_file, write_file, delete_file, clear_workspace, list_files
│   ├── terminal/              # Sandboxed terminal command execution
│   ├── testing/               # Pytest / Jest automated runner
│   └── project/               # Workspace boundary isolation
├── web_app/                   # Neon Genesis Web Studio
│   ├── server.py              # Multi-threaded zero-dependency HTTP server & ZIP packager
│   └── static/                # Web Studio Frontend
│       ├── index.html         # Main Studio UI & Antigravity timer dashboard
│       ├── about.html         # System documentation & owner info
│       ├── style.css          # Neon cyberpunk theme & glowing keyframe animations
│       └── app.js             # High-frequency timer engine & API coordinator
├── generated_project/         # Sandbox where synthesized files land
├── main.py                    # Interactive CLI runner
├── pyproject.toml             # Project dependencies & metadata
└── README.md                  # Project documentation
```

---

## 🛡️ License

MIT License — Developed by **Amber Saluja** ([ambersaluja20006@gmail.com](mailto:ambersaluja20006@gmail.com)).

