# 🚀 DevPilot: Autonomous Agentic Software Engineering System
## Comprehensive Project Synopsis & Technical Overview

---

### 📌 Project Metadata
- **Project Name:** DevPilot (Agents v2) & Neon Project Generator
- **Project Owner:** ambersaluja20006@gmail.com
- **Core Frameworks:** LangGraph, LangChain, Groq Cloud API, Google Gemini API
- **Language & Runtime:** Python 3.11+ / `uv` Package Manager
- **Interface:** Modern Cyberpunk / Neon Web Application with Antigravity-style Timers
- **Repository:** `lang_graph_ai_project`

---

## 1. Executive Summary

**DevPilot** is an autonomous, multi-agent AI software engineering framework designed to convert natural language prompts into complete, fully functional, zero-build software projects. Unlike conventional AI coding tools that produce isolated code snippets or single-file scripts without verification, DevPilot implements an end-to-end **Agentic Software Development Life Cycle (SDLC)**. 

Using **LangGraph** to model stateful, cyclical agent interactions, DevPilot autonomously:
1. Classifies user intent (`CREATE`, `MODIFY`, `DEBUG`, `TEST`, `EXPLAIN`, `CHAT`).
2. Inspects existing workspace directory structures and dependencies.
3. Formulates a rigorous software architecture and data-flow model.
4. Breaks down architectural designs into prioritized, actionable task lists.
5. Emits production-grade code files directly into a sandboxed filesystem using tool calling.
6. Runs tests and executes commands to verify functionality.
7. Diagnoses errors and performs automated debugging feedback loops when failures occur.
8. Packages the completed project into a downloadable, zero-build ZIP archive delivered through an interactive neon-themed web dashboard.

---

## 2. Problem Statement

1. **Context Fragmentation in Traditional LLM Code Generators:**
   Standard conversational LLMs hallucinate file references, omit boilerplate, fail to maintain dependencies across files, and cannot interact with the operating system filesystem.
2. **Lack of Automated Verification and Self-Correction:**
   Human developers must manually copy-paste code, test execution, find runtime bugs, and feed stack traces back to the AI.
3. **Over-Engineered Scaffolding vs. Runnability:**
   Many AI tools generate heavy frameworks (e.g., Vite/Webpack/TypeScript) that fail to run because build steps, npm packages, or configuration files are incomplete.
4. **API Rate Limit Bottlenecks (TPM Constraints):**
   Multi-turn autonomous loops frequently blow past provider rate limits (e.g., Groq's 8,000 Tokens-Per-Minute free tier) if agents emit single files over 15+ consecutive turns without context pruning.

---

## 3. Key Objectives

- **Full Lifecycle Automation:** Implement an autonomous multi-agent pipeline replacing manual setup, coding, testing, and packaging.
- **Stateful Directed Graph Workflow:** Use **LangGraph** to maintain a persistent state across agents with conditional routing and dynamic retries.
- **High-Efficiency Batch Generation (Get Shit Done Strategy):** Minimize LLM turns by batching filesystem write operations in parallel, preventing 413/429 rate limit exceptions.
- **Zero-Build, Standalone Deliverables:** Ensure web-based output projects run immediately in any browser via `index.html` without requiring `npm install` or compilation.
- **Antigravity-Inspired User Interface:** Build a zero-dependency web interface featuring cyberpunk aesthetics, real-time node timers, telemetry logs, and a built-in project file inspector.

---

## 4. System Architecture & Agent Pipeline

DevPilot operates as a stateful directed graph (`StateGraph`) where nodes represent specialized agent personas and edges represent routing decisions based on state output.

```
                    ┌─────────────────────────┐
                    │       USER PROMPT       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      ROUTER AGENT       │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │ (CHAT)                │ (CREATE / MODIFY)     │ (EXPLAIN / TEST)
         ▼                       ▼                       ▼
    ┌─────────┐             ┌─────────┐             ┌─────────┐
    │ DIRECT  │             │INSPECTOR│             │EXPLAINER│
    │ RESPONSE│             └────┬────┘             │ / TESTER│
    └─────────┘                  │                  └─────────┘
                                 ▼
                            ┌─────────┐
                            │ARCHITECT│
                            └────┬────┘
                                 │
                                 ▼
                            ┌─────────┐
                            │ PLANNER │
                            └────┬────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │    CODER AGENT    │◄──────────┐
                       └─────────┬─────────┘           │
                                 │                     │ (Retry)
                                 ▼                     │
                       ┌───────────────────┐           │
                       │   TESTER AGENT    │           │
                       └─────────┬─────────┘           │
                                 │                     │
                    ┌────────────┴────────────┐        │
                    │ PASS                    │ FAIL   │
                    ▼                         ▼        │
             ┌──────────────┐          ┌─────────────┐ │
             │ ZIP PACKAGER │          │  DEBUGGER   ├─┘
             └──────┬───────┘          └─────────────┘
                    ▼
             ┌──────────────┐
             │ DOWNLOAD ZIP │
             └──────────────┘
```

### Detailed Agent Responsibilities

| Agent Node | Responsibility | LLM / Mechanism |
| :--- | :--- | :--- |
| **🧭 Router** | Analyzes the input prompt to classify intent: `CREATE`, `MODIFY`, `DEBUG`, `TEST`, or `CHAT`. | Gemini Flash-Lite / Groq Auto |
| **🔍 Inspector** | Inspects the project filesystem, detecting languages, frameworks, existing files, and package manifests. | Filesystem Operations Tool |
| **📐 Architect** | Designs the top-level architecture, module layout, constraints, and data flow. Mandates zero-build standalone structure for web apps. | Groq GPT-OSS 120B (Structured Output) |
| **📋 Planner** | Decomposes architectural designs into 4–7 prioritized tasks. Enforces functional code (`index.html`, `style.css`, `app.js`) as Task 1. | Groq GPT-OSS 120B (Pydantic Schema) |
| **⚡ Coder** | Performs actual code writing using parallel tool calls (`write_file`, `read_file`, `run_cmd`). Implements sliding-window conversation pruning. | Groq Tool-Calling Agent |
| **🧪 Tester** | Discovers tests, executes test suites, parses pass/fail rates, and validates syntax. | Terminal Execution & Test Parser |
| **🛠️ Debugger** | Diagnoses errors and stack traces, reads affected source code, and applies surgical fixes. | Groq Tool-Calling Agent |
| **📦 Packager** | Aggregates generated project files into a compressed ZIP archive available via REST API. | Python `zipfile` in-memory compression |

---

## 5. Technical Innovations & Resilience Strategies

### 1. Zero-Build Standalone Architecture
Instead of generating bloated Node.js boilerplates (`package.json`, `tsconfig.json`, `vite.config.ts`) that require build tools, DevPilot defaults to complete, standalone applications with native HTML5, modern CSS3 (custom properties, flexbox, glassmorphism), and vanilla JavaScript. If libraries like Tailwind or Lucide are needed, they are injected via reliable CDNs. Users can open `index.html` directly in any browser.

### 2. Rate Limit (TPM) Mitigation & Sliding-Window Pruning
To prevent hitting Groq's 8,000 Tokens-Per-Minute free-tier barrier:
- **Batch Tool Generation:** The Coder agent is instructed to emit all primary files in its first turn using parallel tool calls.
- **Sliding-Window Message Pruning:** Conversations exceeding 5 messages are dynamically pruned to keep only the root prompt plus the last 4 turns (~1,200 tokens footprint), leaving massive headroom under the rolling 60-second limit.
- **Multi-Model Failover:** If a model hits a 413 or 429 status code, `invoke_with_retry` applies exponential backoff and automatically falls back to secondary Groq candidates (`gpt-oss-20b`, `groq/compound`) and Google Gemini.

### 3. Antigravity-Style Web Dashboard
- **Real-Time Step Timers:** Tracks the exact execution duration (seconds) of every node in the graph pipeline in real time.
- **Live Terminal Telemetry:** Streams timestamped execution logs directly from the backend server.
- **In-Browser Project File Viewer:** Allows users to inspect generated code files with syntax styling and file size badges before downloading.
- **One-Click Download:** Instant packaging into a clean `.zip` archive.

---

## 6. Technology Stack

- **AI & Agent Orchestration:** LangGraph, LangChain Core, LangChain Groq, LangChain Google GenAI
- **LLMs:** OpenAI GPT-OSS-120B / 20B (via Groq Cloud), Google Gemini 3.5 Flash-Lite
- **Backend Server:** Python 3.11 Standard Library HTTP Server (`http.server`, `threading`, `zipfile`)
- **Frontend Stack:** Semantic HTML5, Vanilla CSS3 (Custom Cyberpunk Glow System), Vanilla ES6 JavaScript
- **Environment & Dependency Management:** `uv` (Fast Python package installer and resolver), `python-dotenv`
- **Version Control & Security:** Git with comprehensive `.gitignore` and automated secret isolation

---

## 7. Results & Verified Outputs

- **Fully Functional Neon Applications:** Generated complex web applications (e.g., Cyberpunk Neon Todo App with local storage and filters, Glassmorphic calculators with history tape) in under 35 seconds.
- **Zero Fatal API Crashes:** Achieved reliable execution without rate-limit interrupts through intelligent pruning and batching.
- **Immediate Portability:** 100% of generated output projects run out-of-the-box without build steps or external dependencies.

---

## 8. Future Roadmap

1. **Dockerized Sandboxing:** Execute untrusted generated code inside isolated micro-containers (Docker / E2B).
2. **Multi-File Refactoring:** Support interactive, conversational diff updates to existing repositories.
3. **One-Click Cloud Deployment:** Integration with Vercel, Netlify, and GitHub Pages APIs.
4. **WebSocket Streaming:** Real-time token streaming directly to the browser UI.

---

*Authored by:* **ambersaluja20006@gmail.com**  
*Project Repository:* **DevPilot / lang_graph_ai_project**
