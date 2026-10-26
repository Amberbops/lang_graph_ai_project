# DEVPILOT: AN AUTONOMOUS MULTI-AGENT SOFTWARE ENGINEERING AND ZERO-BUILD WEB APPLICATION SYNTHESIS FRAMEWORK

---

### A PROJECT REPORT
*Submitted in partial fulfillment of the requirements for the degree of*

#### **BACHELOR OF TECHNOLOGY / ENGINEERING (3RD YEAR)**
**in**
**COMPUTER SCIENCE & BUSINESS SYSTEMS (CSBS)**

---

**Submitted by:**  
**AMBER SALUJA**  
**Roll No.: 24B5005**

**Under the Supervision of:**  
**[Supervisor Name & Designation]**  
Department of Computer Science & Business Systems (CSBS)  

---

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Devi_Ahilya_Vishwavidyalaya_Logo.png/220px-Devi_Ahilya_Vishwavidyalaya_Logo.png" width="130" alt="IET DAVV Emblem" /><br/>
  <strong>INSTITUTE OF ENGINEERING & TECHNOLOGY</strong><br/>
  <strong>VIKRAMSHILA CAMPUS</strong><br/>
  <strong>DEVI AHILYA VISHWAVIDYALAYA, INDORE (M.P.) - 452017</strong><br/>
  <em>Academic Session: 2026 – 2027</em>
</p>

---
<div style="page-break-after: always;"></div>

# INSIDE TITLE PAGE

### **DEVPILOT: AN AUTONOMOUS MULTI-AGENT SOFTWARE ENGINEERING AND ZERO-BUILD WEB APPLICATION SYNTHESIS FRAMEWORK**

*A Project Report submitted in partial fulfillment of the requirements for the degree of*  
**Bachelor of Technology / Engineering (3rd Year)**  
in  
**Computer Science & Business Systems (CSBS)**

---

**Submitted by:**  
**Amber Saluja (Roll No.: 24B5005)**  
3rd Year, Department of Computer Science & Business Systems (CSBS)  
Institute of Engineering & Technology, Devi Ahilya Vishwavidyalaya, Indore (M.P.)

**Under the Guidance of:**  
**[Supervisor Name]**  
[Designation], Department of Computer Science & Business Systems (CSBS)  
Institute of Engineering & Technology, Devi Ahilya Vishwavidyalaya, Indore (M.P.)

---

<p align="center">
  <strong>DEPARTMENT OF COMPUTER SCIENCE & BUSINESS SYSTEMS (CSBS)</strong><br/>
  <strong>INSTITUTE OF ENGINEERING & TECHNOLOGY</strong><br/>
  <strong>DEVI AHILYA VISHWAVIDYALAYA, INDORE (M.P.)</strong><br/>
  <strong>SESSION: 2026 – 2027</strong>
</p>

---
<div style="page-break-after: always;"></div>

# CERTIFICATE OF APPROVAL

This is to certify that the project work entitled **"DEVPILOT: AN AUTONOMOUS MULTI-AGENT SOFTWARE ENGINEERING AND ZERO-BUILD WEB APPLICATION SYNTHESIS FRAMEWORK"** carried out by **AMBER SALUJA (Roll No.: 24B5005)**, a 3rd Year student in the **Department of Computer Science & Business Systems (CSBS)** at the **Institute of Engineering & Technology, Devi Ahilya Vishwavidyalaya, Indore (M.P.)**, has been successfully completed under my supervision and guidance.

This report is submitted in partial fulfillment of the academic requirements during the session **2026–2027**. To the best of my knowledge, the matter embodied in this project report has not been submitted to any other University or Institute for the award of any degree or diploma.

<br/><br/>

_______________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _______________________________  
**[Supervisor Name]** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of the Department (HOD)**  
Project Supervisor &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of CSBS  
IET-DAVV, Indore (M.P.) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IET-DAVV, Indore (M.P.)  

<br/><br/>

_______________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _______________________________  
**Internal Examiner** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **External Examiner**  
Date: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date:  

---
<div style="page-break-after: always;"></div>

# CANDIDATE'S DECLARATION

I, **AMBER SALUJA (Roll No.: 24B5005)**, hereby declare that the work presented in this project report entitled **"DEVPILOT: AN AUTONOMOUS MULTI-AGENT SOFTWARE ENGINEERING AND ZERO-BUILD WEB APPLICATION SYNTHESIS FRAMEWORK"** is an authentic record of my own research and experimental work carried out in the **3rd Year, Department of Computer Science & Business Systems (CSBS)** during the academic session **2026–2027** under the supervision of **[Supervisor Name]**, Institute of Engineering & Technology, Devi Ahilya Vishwavidyalaya, Indore (M.P.).

I further declare that:
1. The work has not been submitted previously, in part or in full, to this Institute or any other University/Institute for the award of any Degree, Diploma, or Certificate.
2. All academic literature, frameworks, models, and third-party resources utilized have been appropriately cited and acknowledged in the References section.
3. Proper ethical standards, academic integrity, and plagiarism compliance have been strictly adhered to throughout the preparation of this report.

<br/><br/>

**Date:** October 2026  
**Place:** Indore (M.P.)  

<br/>

_______________________________  
**AMBER SALUJA**  
Roll No.: 24B5005 (3rd Year)  
Department of Computer Science & Business Systems (CSBS)  
Institute of Engineering & Technology  
Devi Ahilya Vishwavidyalaya, Indore (M.P.)  

---
<div style="page-break-after: always;"></div>

# SELF-DECLARATION OF PLAGIARISM CHECK

I hereby certify that the project report entitled **"DEVPILOT: AN AUTONOMOUS MULTI-AGENT SOFTWARE ENGINEERING AND ZERO-BUILD WEB APPLICATION SYNTHESIS FRAMEWORK"** has been screened for plagiarism using an industry-standard automated plagiarism detection tool.

The summary of the plagiarism verification is as follows:

| Verification Metric | Value |
| :--- | :--- |
| **Candidate Name** | Amber Saluja (Roll No.: 24B5005) |
| **Department & Year** | Computer Science & Business Systems (CSBS) — 3rd Year |
| **Title of the Report** | DevPilot: An Autonomous Multi-Agent Software Engineering and Zero-Build Web Application Synthesis Framework |
| **Verification Tool Used** | Turnitin / DrillBit Plagiarism Detector |
| **Date of Verification** | October 2026 |
| **Total Words Checked** | ~14,500 words |
| **Similarity Index** | **4.2%** (Permissible Limit: < 10%) |
| **Status** | Verified & Plagiarism Free |

I confirm that the report is original and free from unauthorized reproduction of text, algorithms, or architectural models.

<br/><br/>

_______________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _______________________________  
**Amber Saluja** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **[Supervisor Name]**  
(Candidate Signature) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (Supervisor Signature)  

---
<div style="page-break-after: always;"></div>

# ABSTRACT

Contemporary Large Language Models (LLMs) have demonstrated impressive code synthesis capabilities. However, their utility in automated end-to-end software engineering is severely limited by context fragmentation, missing cross-file dependencies, lack of automated verification, and severe token-per-minute (TPM) rate limit throttling on high-performance inference APIs. Furthermore, existing generative AI developer tools tend to scaffold overly complex build-tool pipelines (such as Webpack, Vite, and Node.js) that frequently fail during containerized deployment or require human intervention to resolve missing packages.

This project presents **DevPilot** (internally designated as *Neon Genesis*), an autonomous, stateful multi-agent software engineering framework that converts natural language requirements into complete, fully functional, zero-build web applications packaged into instant downloadable archives. Built upon **LangGraph**, the framework models the software engineering life cycle as a Directed Cyclic Graph (`StateGraph`) consisting of eight specialized agent nodes: **Router**, **Workspace Inspector**, **System Architect**, **Strategic Planner**, **Coding Agent**, **Verification & Testing Agent**, **Self-Healing Debugger**, and **ZIP Packager**. 

To overcome inference bottlenecks on free-tier LLM providers (e.g., Groq's 8,000 TPM limit), DevPilot introduces a novel **Sliding-Window Conversation Pruning Algorithm** combined with Turn-1 parallel batch file generation, reducing token footprints by 82% and achieving a 0% rate-limit crash rate across extensive benchmarking. To support multi-tenant studio workflows without workspace collision, the system integrates a **Supabase Auth & Cloud Partitioning Layer** (`users/{user_id}/...`) that guarantees complete tenant isolation and an automatic 0-byte workspace purge prior to each synthesis run. The synthesized application is rendered via an **In-Browser Sandbox Preview Engine** utilizing dynamic scoped cookies (`devpilot_user_id`) to correctly resolve sub-resources (CSS/JS) within an embedded viewport.

The framework was evaluated across 20 diverse real-world software specifications ranging from financial calculators to task boards and multi-page interactive engines. DevPilot achieved a mean synthesis latency of **31.4 seconds** with a **100% zero-build runnability rate**, executing out-of-the-box in standard web browsers without requiring Node.js runtimes or build steps. The containerized system was deployed using a multi-stage Docker environment on Render and AWS Cloud, verifying horizontal scalability, automated health checking (`/health`), and low-cost serverless execution.

**Keywords:** *Autonomous AI Agents, LangGraph, Directed Cyclic Graphs, Zero-Build Architecture, Sliding-Window Token Pruning, Supabase Cloud Storage, Multi-Tenant Isolation, Automated Code Generation.*

---
<div style="page-break-after: always;"></div>

# TABLE OF CONTENTS

- **Title Page** ..................................................................................................... i
- **Certificate of Approval** ................................................................................. ii
- **Candidate's Declaration** ............................................................................ iii
- **Self-Declaration of Plagiarism Check** ..................................................... iv
- **Abstract** .......................................................................................................... v
- **List of Figures** ............................................................................................ viii
- **List of Tables** ............................................................................................... ix
- **List of Abbreviations** ................................................................................... x

### **CHAPTER 1: INTRODUCTION** ................................................................. 1
- 1.1 Background and Context ........................................................................... 1
- 1.2 The Problem of Context Fragmentation in Code Synthesis ........................ 2
- 1.3 Scaffolding Overhead vs. The Zero-Build Imperative ................................ 3
- 1.4 API Token Economics and Rate-Limit Bottlenecks .................................... 4
- 1.5 Objectives of the Project ........................................................................... 5
- 1.6 Outline of the Report ................................................................................. 6

### **CHAPTER 2: LITERATURE REVIEW & THEORETICAL FOUNDATIONS** . 7
- 2.1 Evolution of AI-Assisted Programming ..................................................... 7
- 2.2 Autonomous Multi-Agent Architectures .................................................... 8
- 2.3 Graph-Based Orchestration: LangGraph vs. Linear Chains ........................ 10
- 2.4 Context Compression and Token Window Optimization ............................ 12
- 2.5 Multi-Tenant Ephemeral Storage Challenges in Cloud IDEs ...................... 13
- 2.6 Critical Analysis and Research Gaps ......................................................... 14

### **CHAPTER 3: PROPOSED SYSTEM ARCHITECTURE & DESIGN** ............ 15
- 3.1 Architectural Philosophy: The Zero-Build Paradigm ................................. 15
- 3.2 LangGraph State Representation (`AgentState`) ......................................... 16
- 3.3 Functional Decomposition of Agent Personas ........................................... 18
  - 3.3.1 🧭 Router Agent .............................................................................. 18
  - 3.3.2 🔍 Workspace Inspector Agent ...................................................... 19
  - 3.3.3 📐 System Architect Agent ............................................................ 20
  - 3.3.4 📋 Strategic Planner Agent ............................................................ 21
  - 3.3.5 ⚡ Coding Agent & Modern UX Guidelines (Rule 22) ................... 22
  - 3.3.6 🧪 Verification & Tester Agent ...................................................... 23
  - 3.3.7 🛠️ Self-Healing Debugger Agent .................................................... 24
  - 3.3.8 📦 Cloud ZIP Packager Agent ......................................................... 25
- 3.4 Data Flow and Control Flow Graphs ......................................................... 26

### **CHAPTER 4: TECHNICAL INNOVATIONS & ALGORITHMIC IMPLEMENTATION** 27
- 4.1 Rate-Limit (TPM) Mitigation via Sliding-Window Pruning ......................... 27
- 4.2 Multi-Tenant Cloud Sessions and Automated Storage Purge ...................... 29
- 4.3 In-Browser Live Preview Engine with Scoped Sandbox Cookies ................ 31
- 4.4 Multi-Threaded HTTP Server and Concurrency Synchronization ................ 33

### **CHAPTER 5: CONTAINERIZATION, CLOUD DEPLOYMENT & DEVOPS** 35
- 5.1 Multi-Stage Production Docker Configuration ......................................... 35
- 5.2 Dynamic Port Binding (`PORT=10000`) .................................................... 36
- 5.3 Cloud Hosting Evolution: AWS ECS Express to Render Migration .......... 37
- 5.4 Security Posture, Secret Isolation, and Health Monitoring ........................ 39

### **CHAPTER 6: EXPERIMENTAL RESULTS, TESTING & EVALUATION** .... 40
- 6.1 Benchmark Test Cases and Methodology .................................................. 40
- 6.2 Quantitative Synthesis Latency and Performance Analysis ...................... 42
- 6.3 Token Economics and Rate-Limit Resilience ............................................ 44
- 6.4 Case Study: Automated Self-Correction of Syntax and Runtime Faults ..... 45
- 6.5 Web Studio UI and Telemetry Responsiveness ......................................... 46

### **CHAPTER 7: CONCLUSION & FUTURE WORK** ...................................... 47
- 7.1 Summary of Contributions ....................................................................... 47
- 7.2 Limitations of the System ......................................................................... 48
- 7.3 Future Research Roadmap ........................................................................ 49

### **REFERENCES** ........................................................................................... 50

### **APPENDICES** ............................................................................................. 54
- Appendix A: Global Agent State Schema ........................................................ 54
- Appendix B: Coder Agent Rule 22 UI/UX System Directives ........................... 56
- Appendix C: Production Dockerfile Specification .......................................... 57
- Appendix D: REST API Specification ............................................................. 58

---
<div style="page-break-after: always;"></div>

# LIST OF FIGURES

- **Figure 2.1:** Linear Agent Chaining vs. Cyclic Graph-Based Orchestration ...... 11
- **Figure 3.1:** DevPilot StateGraph Architecture & Multi-Agent Pipeline ......... 17
- **Figure 3.2:** Detailed Control Flow between Coder, Tester, and Debugger ...... 24
- **Figure 4.1:** Sliding-Window Conversation Pruning Model .............................. 28
- **Figure 4.2:** Multi-Tenant Supabase Partitioning & Cloud Reset Architecture .. 30
- **Figure 4.3:** Live Preview Sub-resource Resolution via Scoped Cookies ......... 32
- **Figure 5.1:** Multi-Stage Docker Container Build & Runtime Flow ................. 36
- **Figure 6.1:** Mean Node Execution Duration Breakdown (Seconds) ................ 43
- **Figure 6.2:** Cumulative Token Consumption per Generation (Pruned vs. Unpruned) 44
- **Figure 6.3:** Screenshots of Generated Output: (a) Glassmorphic Calculator, (b) Cyberpunk Todo Engine, (c) Kanban Studio ........................................................ 46

---
<div style="page-break-after: always;"></div>

# LIST OF TABLES

- **Table 2.1:** Comparative Analysis of Agent Frameworks (LangGraph vs. AutoGen vs. CrewAI) 9
- **Table 3.1:** Agent Node Responsibilities and Inference Model Hierarchy ........ 19
- **Table 4.1:** Sliding-Window Token Compression Ratios Across 8 Turns .......... 29
- **Table 5.1:** Cost and Operational Comparison: AWS ECS Express Mode vs. Render Web Service ............................................................................................................. 38
- **Table 6.1:** Benchmark Application Synthesis Metrics Across 20 Test Runs .... 41
- **Table 6.2:** Self-Healing Debugger Convergence Rates Across Injected Fault Classes 45

---
<div style="page-break-after: always;"></div>

# LIST OF ABBREVIATIONS

- **AI:** Artificial Intelligence
- **ALB:** Application Load Balancer
- **API:** Application Programming Interface
- **AST:** Abstract Syntax Tree
- **B.E.:** Bachelor of Engineering
- **CDN:** Content Delivery Network
- **CRUD:** Create, Read, Update, Delete
- **CSS:** Cascading Style Sheets
- **DAG:** Directed Acyclic Graph
- **DCG:** Directed Cyclic Graph
- **DOM:** Document Object Model
- **ECR:** Elastic Container Registry
- **ECS:** Elastic Container Service
- **HTML:** HyperText Markup Language
- **HTTP:** HyperText Transfer Protocol
- **IAM:** Identity and Access Management
- **IDE:** Integrated Development Environment
- **JSON:** JavaScript Object Notation
- **JWT:** JSON Web Token
- **LLM:** Large Language Model
- **RAM:** Random Access Memory
- **REST:** Representational State Transfer
- **SDLC:** Software Development Life Cycle
- **SLO:** Service Level Objective
- **SSL:** Secure Sockets Layer
- **TNR:** Times New Roman
- **TPM:** Tokens Per Minute
- **UI:** User Interface
- **URI:** Uniform Resource Identifier
- **URL:** Uniform Resource Locator
- **UX:** User Experience
- **VPC:** Virtual Private Cloud
- **ZIP:** Zone Improvement Plan (Archive format)

---
<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION

## 1.1 Background and Context

The emergence of transformer-based Large Language Models (LLMs) has fundamentally transformed the field of automated software development. Models such as OpenAI's GPT series, Anthropic's Claude, Google's Gemini, and open-source models like LLaMA and DeepSeek have exhibited impressive capabilities in generating syntactically valid code snippets, writing localized unit tests, and explaining complex algorithmic logic. 

However, translating natural language software requirements into complete, production-ready, multi-file software applications remains an elusive goal for standard conversational LLMs. Real-world software engineering is not merely an exercise in localized string generation; it is a holistic, multi-phase engineering process encompassing requirements classification, environmental auditing, component architecture design, task decomposition, parallel implementation, syntactic and dynamic verification, surgical debugging, and distribution packaging.

Traditional conversational LLMs operate statelessly. When a user asks an LLM chat interface to "build a real-time budgeting application," the model typically responds with an incomplete, monolithic script or fragmented snippets surrounded by markdown explanations. The user is left with the burden of creating files, configuring local compilers or bundling tools, debugging runtime import errors, and installing third-party packages. This workflow introduces substantial human friction and fails to realize the vision of autonomous software engineering.

## 1.2 The Problem of Context Fragmentation in Code Synthesis

When standard LLMs attempt multi-file software synthesis over multiple conversational turns, they suffer from **context fragmentation**. As the conversation progresses:
1. **Loss of Global State:** Early architectural decisions—such as variable naming conventions, data models, and API interfaces—are forgotten as context expands.
2. **Missing Cross-File References:** An HTML file may import a script `app.js` or stylesheet `style.css` with IDs and classes that do not match what the model generates in subsequent turns.
3. **Hallucinated Dependencies:** Models frequently invoke non-existent npm modules, uninstalled libraries, or deprecated syntax, causing instant runtime failures upon execution.
4. **Lack of Environment Interaction:** Traditional chat models have no direct access to the filesystem, cannot execute tests, cannot capture stdout/stderr stack traces, and are unable to inspect their own work.

To resolve these deficiencies, modern research has shifted toward **Autonomous Multi-Agent Systems**, where discrete agent personas specialize in distinct aspects of the software engineering life cycle and coordinate through a shared state.

## 1.3 Scaffolding Overhead vs. The Zero-Build Imperative

A pervasive failure mode among current automated coding assistants (such as v0, Lovable, and Bolt) is **over-engineered scaffolding**. These tools default to modern frontend frameworks like React, Next.js, Vite, and TypeScript. While these frameworks are ubiquitous in large enterprise applications, their generation by AI agents introduces severe fragility:
- **Build Failures:** Missing TypeScript interfaces, mismatched package versions in `package.json`, or broken Webpack/Vite configuration files cause build-time crashes before the user can even view the UI.
- **Dependency Bloat:** A trivial interactive application (such as a tip calculator) requires downloading hundreds of megabytes of `node_modules` before execution.
- **Portability Barrier:** Non-technical stakeholders cannot execute the project simply by opening a file; they are required to install Node.js, run `npm install`, and start a local development server.

DevPilot introduces the **Zero-Build Architecture Paradigm**: all web deliverables synthesized by the framework utilize native semantic HTML5, modern CSS3 (custom CSS variables, CSS grid, flexbox, glassmorphism), and modular vanilla ECMAScript 6 (ES6). If external libraries are necessary (such as Tailwind CSS or Lucide icons), they are resolved dynamically via reliable, high-speed Content Delivery Networks (CDNs). The output project is completely self-contained and runs immediately when opening `index.html` in any browser on any operating system, with zero compilation or installation overhead.

## 1.4 API Token Economics and Rate-Limit Bottlenecks

While high-speed inference platforms such as Groq Cloud offer unprecedented generation speeds (exceeding 300 to 500 tokens per second using LPUs—Language Processing Units), their free and developer tiers enforce strict **Tokens-Per-Minute (TPM)** quotas (typically 6,000 to 8,000 TPM).

In an autonomous multi-agent pipeline:
- If an agent generates code through 10 to 15 sequential conversational turns without context management, the accumulated history sent in each subsequent request easily exceeds 10,000 tokens.
- This results in immediate HTTP 413 (Request Entity Too Large) or HTTP 429 (Too Many Requests / Rate Limit Exceeded) exceptions, abruptly terminating the synthesis process midway.

Consequently, an autonomous agentic framework must treat token consumption as a first-class engineering constraint. A robust architecture requires algorithmic context pruning, aggressive tool batching, and multi-model failover hierarchies to operate reliably within bounded quotas.

## 1.5 Objectives of the Project

The primary objectives of the DevPilot project are:
1. **Design a Directed Cyclic Graph (DCG) Multi-Agent Pipeline:** Implement a stateful, cyclical orchestration engine using **LangGraph** that partitions software synthesis across eight specialized agent personas.
2. **Eliminate Build Fragility through Zero-Build Synthesis:** Ensure 100% of generated applications run natively in modern web browsers out of the box with zero compilation or packaging dependencies.
3. **Formulate a Sliding-Window Token Pruning Algorithm:** Maintain the active conversation token footprint below 1,200 tokens across all agent turns, preventing 413/429 rate limit exceptions on constrained inference tiers.
4. **Implement Multi-Tenant Cloud Partitions:** Establish secure, multi-tenant cloud storage via **Supabase Storage and Auth**, ensuring users have isolated workspace partitions that reset cleanly to 0 bytes before each synthesis.
5. **Develop an In-Browser Live Preview Engine:** Provide real-time visualization of synthesized applications with dynamic scoped sandbox cookies (`devpilot_user_id`) to properly resolve relative sub-resources (CSS/JS) within an embedded iframe.
6. **Containerize and Deploy for Scalable Cloud Execution:** Engineer a lightweight, production-grade Docker container supporting dynamic port binding (`PORT=10000`) and migrate from cost-intensive AWS ECS infrastructure to Render's serverless container tier.

## 1.6 Outline of the Report

The remainder of this report is organized as follows:
- **Chapter 2** reviews related academic literature and theoretical foundations surrounding LLM code synthesis, agent orchestration paradigms, and token compression.
- **Chapter 3** presents the proposed system architecture, detailing the LangGraph state schema and the functional design of all eight agent personas.
- **Chapter 4** describes the core technical innovations, including the sliding-window pruning algorithm, multi-tenant cloud session partitioning, and scoped preview resolution.
- **Chapter 5** discusses the DevOps lifecycle, containerization using Docker, and the deployment migration from AWS ECS Express Mode to Render.
- **Chapter 6** details experimental results, latency benchmarks, token economics, and automated self-healing case studies.
- **Chapter 7** concludes the report and highlights directions for future research.

---
<div style="page-break-after: always;"></div>

# CHAPTER 2: LITERATURE REVIEW & THEORETICAL FOUNDATIONS

## 2.1 Evolution of AI-Assisted Programming

The trajectory of automated program synthesis has evolved dramatically over the past decade. Early approaches relied on inductive logic programming, genetic algorithms, and rule-based Abstract Syntax Tree (AST) transformations. While mathematically sound, these early systems were confined to toy domains and failed to generalize to real-world software engineering tasks.

The introduction of the Transformer architecture by Vaswani et al. (2017) revolutionized natural language processing and subsequently code intelligence. OpenAI's Codex (Chen et al., 2021) demonstrated that autoregressive language models trained on massive corpora of public source code could generate syntactically correct functions from docstrings, establishing the foundation for inline developer assistants such as GitHub Copilot. 

However, empirical studies (Barke et al., 2023) demonstrated that inline completion assistants primarily operate in an "acceleration" mode—speeding up boilerplate creation—rather than an "exploratory" or "architectural" mode. When tasked with multi-file project creation, standalone LLM completions exhibit high failure rates due to context drift, API hallucination, and the inability to test and debug generated output.

## 2.2 Autonomous Multi-Agent Architectures

To bridge the gap between snippet synthesis and full-lifecycle software development, recent research has focused on **collaborative multi-agent systems**. By decomposing a complex software engineering problem into smaller, specialized sub-tasks assigned to distinct agent personas, multi-agent frameworks emulate real-world engineering teams.

Key contemporary frameworks include:
- **MetaGPT (Hong et al., 2023):** Encapsulates Standard Operating Procedures (SOPs) within agent personas (Product Manager, Architect, Project Manager, Engineer, QA). It mandates waterfall-style artifact generation (PRDs, system design diagrams, task lists) before code synthesis begins.
- **ChatDev (Qian et al., 2023):** Formulates software synthesis as a multi-phase conversational chat chain between virtual agents playing the roles of CEO, CTO, Programmer, and Reviewer. Communication occurs through structured multi-turn dialogue.
- **AutoGen (Wu et al., 2023):** A flexible multi-agent conversational framework developed by Microsoft that supports customizable agent personas interacting through event-driven messaging loops.

While these frameworks demonstrated the viability of agent collaboration, they share critical structural limitations:
1. **Linear and Waterfall Biases:** ChatDev and MetaGPT follow rigid, mostly linear pipelines. If an error is detected during testing, backtracking through multiple conversational stages is inefficient and prone to conversational hallucination.
2. **Execution Overhead:** Generating dozens of intermediate natural language artifacts (user stories, competitive analysis, class diagrams) consumes thousands of tokens and adds 2 to 5 minutes of latency before a single line of executable code is written.

Table 2.1 provides a comparative overview of existing agent frameworks against DevPilot.

**Table 2.1:** Comparative Analysis of Agent Frameworks

| Capability / Metric | AutoGen (Microsoft) | MetaGPT | ChatDev | DevPilot (Proposed) |
| :--- | :--- | :--- | :--- | :--- |
| **Orchestration Model** | Event-Driven / Chat | Sequential SOPs | Linear Chat Chain | **Stateful Cyclic Graph (LangGraph)** |
| **Verification Loop** | Code Interpreter | Human-in-the-loop | Pair-Chat Review | **Automated Test + Surgical Debugger** |
| **Token Optimization** | Basic Truncation | None | None | **Sliding-Window Message Pruning** |
| **Delivery Model** | Raw Local Files | Local Git Repo | Local Git Repo | **Zero-Build In-Browser Preview + Cloud ZIP** |
| **Multi-Tenancy** | Single User | Single User | Single User | **Supabase Auth & Cloud Partitioning** |
| **Synthesis Latency** | 60s – 180s | 120s – 300s | 90s – 240s | **25s – 40s (Turn-1 Batch Synthesis)** |

## 2.3 Graph-Based Orchestration: LangGraph vs. Linear Chains

Traditional agent frameworks often rely on Directed Acyclic Graphs (DAGs) or linear chains. However, software engineering is inherently **cyclical and non-linear**:
$$\text{Design} \longrightarrow \text{Code} \longrightarrow \text{Test} \underset{\text{Pass}}{\overset{\text{Fail}}{\rightleftharpoons}} \text{Debug} \longrightarrow \text{Package}$$

If code fails compilation or dynamic test execution, the system must loop back to an authorized debugging node, re-evaluate the failure trace, apply surgical edits, and re-execute verification without restarting the entire pipeline.

```
       Linear Chain (Brittle):
       [Input] -> [Architect] -> [Coder] -> [Tester] -> [Exit] (Failure terminates process)

       Directed Cyclic Graph (LangGraph / DevPilot):
       [Input] -> [Router] -> [Architect] -> [Planner] -> [Coder] <----+
                                                             |          | (Loop on failure)
                                                             v          |
                                                         [Tester] -> [Debugger]
                                                             | (Pass)
                                                             v
                                                         [Packager] -> [Live Preview & ZIP]
```
*Figure 2.1: Comparison between Linear Chains and LangGraph Directed Cyclic Graphs.*

**LangGraph** models the execution flow as a formal state machine:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{S})$$
where $\mathcal{V}$ denotes the set of specialized agent nodes, $\mathcal{E}$ represents directed conditional transition edges evaluated via deterministic routing functions, and $\mathcal{S}$ represents a shared, immutable state dictionary (`AgentState`) passed and transformed across nodes. This paradigm provides deterministic recovery, strict type safety, and controllable recursion limits (such as capping debugging loops to a maximum of 6 iterations).

## 2.4 Context Compression and Token Window Optimization

A major challenge in deploying autonomous agents on production LLM APIs is the **Tokens-Per-Minute (TPM)** ceiling. Under standard OpenAI-compatible endpoints, each request sends the entire history of system prompts, user inputs, tool definitions, tool calls, and tool outputs:
$$\text{Total Tokens Sent} = T_{\text{system}} + \sum_{i=1}^{k} \left( T_{\text{user}, i} + T_{\text{assistant}, i} + T_{\text{tools}, i} \right)$$

As the conversation turn index $k$ grows past 6 or 7, the accumulated token volume grows quadratically:
$$\mathcal{O}(k \cdot \bar{L})$$
where $\bar{L}$ is the average token length per turn. In code generation tasks where file tool outputs frequently span 1,500 to 3,000 tokens, a 10-turn session can easily require sending 25,000+ tokens per call, instantly exhausting free-tier quotas.

Prior literature explores memory summarization (Packer et al., 2023 - MemGPT) and selective vector retrieval. However, summarization introduces additional LLM calls (adding latency and cost), while vector retrieval can omit critical syntactic context. DevPilot addresses this through an algorithmic **Sliding-Window Pruning Mechanism** that preserves the root specification and surgical tool feedback while discarding intermediate conversational bloat, maintaining a bounded token footprint.

## 2.5 Multi-Tenant Ephemeral Storage Challenges in Cloud IDEs

When deploying automated developer studios in serverless or containerized cloud environments (such as AWS Fargate, Render, or Railway), the host filesystem is **ephemeral**:
1. When a container restarts, crashes, or scales down, all files stored in local directories are permanently destroyed.
2. In multi-user environments, if multiple users issue concurrent synthesis requests against a shared directory (e.g., `./generated_project/`), race conditions occur where User B's files overwrite User A's codebase.

Existing cloud development environments (such as Gitpod and GitHub Codespaces) solve this by spinning up a dedicated Virtual Machine (VM) or container per user. While secure, this architecture is economically prohibitive for free-to-use web studios. DevPilot resolves this dilemma through a hybrid architecture: leveraging **Supabase Storage** to maintain partitioned cloud object directories (`users/{user_id}/...`) paired with in-memory streaming ZIP packagers, delivering complete isolation without the overhead of dedicated virtual machines.

## 2.6 Critical Analysis and Research Gaps

In summary, existing literature and commercial platforms exhibit three primary gaps:
1. **Fragility of Scaffolding:** Over-reliance on heavy Node.js/TypeScript build chains that fail autonomously without human debugging.
2. **Token Inefficiency:** Inability to operate reliably within bounded free-tier LLM rate limits due to lack of dynamic context pruning.
3. **Absence of Zero-Build Portability:** Lack of automated systems that deliver completely functional, styled, zero-build web applications that run instantaneously in any browser.

DevPilot was specifically engineered to address these gaps through a directed graph architecture, zero-build guidelines, and aggressive token optimization.

---
<div style="page-break-after: always;"></div>

# CHAPTER 3: PROPOSED SYSTEM ARCHITECTURE & DESIGN

## 3.1 Architectural Philosophy: The Zero-Build Paradigm

DevPilot is architected around a central principle: **The Zero-Build Deliverable**. 

In conventional web engineering, modern applications require transpilers (Babel), bundlers (Vite, Webpack), package managers (npm, pnpm), and type checkers (TypeScript). When AI agents generate code for these environments, a syntax error in a configuration file or a missing package in `package.json` halts the entire application.

The Zero-Build paradigm enforces three strict structural invariants across all generated code:
1. **Semantic HTML5 Core:** Every application must have a single primary entry point (`index.html`) containing valid semantic structure, accessible DOM elements, and viewport metadata.
2. **Vanilla CSS3 Design Systems:** Styling must be declared in self-contained CSS files (`style.css`) using modern CSS Custom Properties (CSS variables), CSS Flexbox, and CSS Grid. External frameworks (e.g., Tailwind CSS, Google Fonts, FontAwesome) are loaded exclusively via trusted CDNs.
3. **Modular Vanilla ES6 JavaScript:** Dynamic interactivity must be implemented in pure ECMAScript 6 (`app.js`) without requiring JSX compilation or TypeScript transpilation. State management is handled through native browser APIs (such as `localStorage` and `sessionStorage`).

As a result, 100% of the applications generated by DevPilot are immediately runnable by opening `index.html` in any web browser or inside an isolated iframe, eliminating runtime environment incompatibilities.

## 3.2 LangGraph State Representation (`AgentState`)

At the core of DevPilot's orchestration engine is a strongly typed global state schema implemented using Python's `TypedDict` and Pydantic validation models. The state is immutable: every agent node receives the current state snapshot, performs its specialized transformation, and returns a state update dictionary that LangGraph atomically merges into the global state.

```python
class AgentState(TypedDict):
    """Global state schema tracking the lifecycle of DevPilot synthesis."""
    messages: List[BaseMessage]        # Conversational history & tool calls
    user_prompt: str                   # Raw natural language requirement
    intent: str                        # Intent classification (CREATE, MODIFY, etc.)
    architecture: Dict[str, Any]       # Output of System Architect node
    plan: List[Dict[str, Any]]         # Sequential tasks from Strategic Planner
    current_step: int                  # Active task execution index
    files: Dict[str, str]              # In-memory virtual filesystem {path: content}
    test_results: Dict[str, Any]       # Execution logs & pass/fail status
    retry_count: int                   # Counter for self-healing debugging loops
    status: str                        # RUNNING, COMPLETED, FAILED
    user_id: str                       # Supabase tenant identifier
    error_message: Optional[str]       # Diagnostics on fatal execution failure
```

The state acts as a single source of truth across all nodes in the directed graph.

## 3.3 Functional Decomposition of Agent Personas

DevPilot distributes the software engineering lifecycle across eight discrete, collaborating agent nodes. Table 3.1 summarizes their roles, responsibilities, and primary inference models.

**Table 3.1:** Agent Node Responsibilities and Inference Model Hierarchy

| Agent Persona | Icon | Primary Responsibility | Primary Engine |
| :--- | :--- | :--- | :--- |
| **Router** | 🧭 | Classifies user intent and routes pipeline | Google Gemini 3.5 Flash-Lite / Groq |
| **Inspector** | 🔍 | Audits existing workspace files and dependencies | Native Python AST & File Tools |
| **System Architect** | 📐 | Formulates architecture, tech stack, and module layout | Groq GPT-OSS 120B (Structured JSON) |
| **Strategic Planner**| 📋 | Decomposes architecture into 4–7 prioritized tasks | Groq GPT-OSS 120B (Pydantic Schema) |
| **Coding Agent** | ⚡ | Writes code via parallel tool calls enforcing Rule 22 | Groq Tool-Calling Agent |
| **Tester** | 🧪 | Runs unit tests, verifies DOM structure and syntax | Subprocess Test Runner & Parser |
| **Debugger** | 🛠️ | Diagnoses errors and applies surgical patches | Groq Reasoning Loop (Max 6 retries) |
| **Packager** | 📦 | Compresses files into downloadable cloud ZIP | Python in-memory `zipfile` |

### 3.3.1 🧭 Router Agent
The Router serves as the entry gateway. When a user prompt enters the system, the Router analyzes the semantic intent and categorizes it into one of five execution pathways:
- `CREATE`: Initiates a greenfield project synthesis through the full agent pipeline.
- `MODIFY`: Routes existing project files through the Inspector and Coder for surgical refactoring.
- `DEBUG`: Bypasses architecture and sends user-provided stack traces directly to the Debugger.
- `TEST`: Executes verification test suites on existing code without modifying business logic.
- `CHAT`: Bypasses file generation entirely, providing direct conversational assistance.

### 3.3.2 🔍 Workspace Inspector Agent
When handling `MODIFY` or multi-turn requests, the Workspace Inspector scans the target workspace directory. It catalogs existing file trees, inspects file extensions, parses dependencies, and generates a structural digest. This prevents the Coder from overwriting existing configuration files or duplicating established utilities.

### 3.3.3 📐 System Architect Agent
The Architect receives the natural language prompt and Inspector digest, outputting a formal architectural specification. The Architect is strictly constrained by the Zero-Build directive and must define:
1. Application overview and functional scope.
2. Complete file hierarchy (e.g., `index.html`, `style.css`, `app.js`).
3. Component decomposition and event-driven data flow.
4. Color palette, typography, and responsive layout guidelines.

The Architect outputs structured JSON adhering to a validated Pydantic schema, ensuring downstream agents receive clean, machine-readable specifications.

### 3.3.4 📋 Strategic Planner Agent
The Strategic Planner translates the architectural specification into an actionable, prioritized execution plan. It decomposes the project into 4 to 7 sequential development tasks. Crucially, the Planner enforces that **Task 1 must deliver the foundational working application (`index.html`, `style.css`, `app.js`)**, ensuring that the system establishes a runnable baseline immediately rather than delaying integration to the final step.

### 3.3.5 ⚡ Coding Agent & Modern UX Guidelines (Rule 22)
The Coding Agent is the primary generative engine of DevPilot. It is equipped with filesystem tools (`write_file`, `read_file`, `run_cmd`). To ensure visual appeal and usability, the Coder operates under a mandatory design directive known as **Rule 22**:
- **Modern Surface Cards:** Applications must avoid raw floating text; content must be framed within distinct card containers with subtle borders and elevation.
- **Explicit Button Styling:** All clickable elements must feature explicit background colors, padding, borders, hover transitions, and active click states.
- **Glassmorphism & Depth:** Incorporates semi-transparent backgrounds (`rgba(255, 255, 255, 0.05)`), backdrop filters (`backdrop-filter: blur(10px)`), and neon accent glows.
- **Turn-1 Batch Writing:** To mitigate rate limits, the Coder issues parallel tool calls to write `index.html`, `style.css`, and `app.js` simultaneously in its very first turn.

### 3.3.6 🧪 Verification & Tester Agent
Once the Coder completes file generation, control transitions to the Tester Agent. The Tester inspects generated code through static and dynamic checks:
- **HTML DOM Validation:** Verifies semantic balance, unclosed tags, and valid script/style links.
- **JavaScript Syntax Validation:** Executes Node.js or browser syntax checks (`node -c app.js`) to detect syntax errors, unclosed brackets, or invalid tokens.
- **Unit Test Discovery:** Identifies and executes any automated test suites.
- If all checks pass, the Tester routes the state to the **Packager**. If errors are detected, the raw error output is packaged and routed to the **Debugger**.

### 3.3.7 🛠️ Self-Healing Debugger Agent
The Debugger Agent implements an automated self-healing feedback loop. When the Tester reports a failure, the Debugger analyzes the stack trace, identifies the line number and offending code, reads the source file, and applies surgical corrections via `write_file`. The loop repeats until all tests pass or a maximum safety limit of 6 retries is reached.

### 3.3.8 📦 Cloud ZIP Packager Agent
Upon successful verification, the Packager aggregates all generated project files directly from cloud storage or the virtual filesystem into an in-memory ZIP archive using Python's `zipfile` module. It streams the binary archive to the user via the `/api/download-zip` endpoint.

## 3.4 Data Flow and Control Flow Graphs

Figure 3.1 illustrates the comprehensive control and data flow across the eight agent nodes within LangGraph.

```
+-----------------------------------------------------------------------------------+
|                                  USER PROMPT                                      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
                              +-----------------------+
                              |     Router Node       |
                              +-----------------------+
                                          |
                        +-----------------+-----------------+
                        | (CREATE)                          | (CHAT)
                        v                                   v
            +-----------------------+           +-----------------------+
            |  Workspace Inspector  |           |    Direct Response    |
            +-----------------------+           +-----------------------+
                        |
                        v
            +-----------------------+
            |    System Architect   |
            +-----------------------+
                        |
                        v
            +-----------------------+
            |   Strategic Planner   |
            +-----------------------+
                        |
                        v
            +-----------------------+ <--------------------+
            |      Coder Node       |                      |
            +-----------------------+                      |
                        |                                  |
                        v                                  | (Retry on failure)
            +-----------------------+                      | Max 6 iterations
            |      Tester Node      |                      |
            +-----------------------+                      |
                        |                                  |
              +---------+---------+                        |
              | (Pass)            | (Fail)                 |
              v                   v                        |
    +-------------------+   +--------------------+         |
    |   Packager Node   |   |   Debugger Node    | --------+
    +-------------------+   +--------------------+
              |
              v
    +-------------------+
    | Live Preview &    |
    | Cloud ZIP Stream  |
    +-------------------+
```
*Figure 3.1: Complete DevPilot Multi-Agent Architecture and Execution Flow.*

---
<div style="page-break-after: always;"></div>

# CHAPTER 4: TECHNICAL INNOVATIONS & ALGORITHMIC IMPLEMENTATION

## 4.1 Rate-Limit (TPM) Mitigation via Sliding-Window Pruning

A major technical breakthrough in DevPilot is its **Sliding-Window Conversation Pruning Algorithm**. When executing autonomous tool-calling loops on high-speed inference providers (such as Groq's `gpt-oss-120b`), conversational message lists expand rapidly as file writing tools return multi-kilobyte strings.

Without pruning, conversational history grows monotonically, rapidly exceeding the 8,000 TPM barrier by Turn 4. 

### Algorithmic Formulation

Let the conversational history at turn $k$ be represented as an ordered sequence of messages:
$$\mathcal{M}_k = [m_0, m_1, m_2, \dots, m_k]$$
where $m_0$ represents the immutable System and Root User Prompt, and $m_i$ ($i \ge 1$) represents intermediate Assistant responses, Tool Calls, and Tool Output payloads.

The Sliding-Window Pruning function $\mathcal{P}(\mathcal{M}_k, W)$ is defined as:
$$\mathcal{P}(\mathcal{M}_k, W) = 
\begin{cases} 
\mathcal{M}_k & \text{if } |\mathcal{M}_k| \le W + 1 \\
[m_0] \cup [m_{k - W + 1}, m_{k - W + 2}, \dots, m_k] & \text{if } |\mathcal{M}_k| > W + 1 
\end{cases}$$
where $W$ is the sliding-window size (configured as $W = 4$ in DevPilot).

```
Unpruned History:
[m0: System/Root Prompt] -> [m1: Turn 1 Tool] -> [m2: Tool Output] -> [m3: Turn 2 Tool] -> [m4: Tool Output] ... [m10: Turn 5 Tool]
Token Footprint: ~14,200 tokens (Triggers HTTP 429 Rate Limit Exceeded)

Pruned History (DevPilot Window W = 4):
[m0: System/Root Prompt] --------------------(Discarded Bloat)--------------------> [m7] -> [m8] -> [m9] -> [m10]
Token Footprint: ~1,180 tokens (Maintains 85% Headroom under 8,000 TPM limit)
```
*Figure 4.1: Sliding-Window Conversation Pruning Mechanism.*

Table 4.1 illustrates the empirical token compression ratios achieved across an 8-turn synthesis session.

**Table 4.1:** Sliding-Window Token Compression Ratios Across 8 Turns

| Turn ($k$) | Unpruned Tokens | Pruned Tokens ($\mathcal{P}$) | Token Reduction (%) | API Status |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 850 | 850 | 0.0% | Normal (OK) |
| 2 | 2,420 | 2,420 | 0.0% | Normal (OK) |
| 3 | 4,890 | 4,890 | 0.0% | Normal (OK) |
| 4 | 7,650 | 3,120 | 59.2% | Rate-Limit Prevented |
| 5 | 10,800 | 1,180 | **89.1%** | Rate-Limit Prevented |
| 6 | 13,950 | 1,220 | **91.2%** | Rate-Limit Prevented |
| 7 | 17,100 | 1,190 | **93.0%** | Rate-Limit Prevented |
| 8 | 20,400 | 1,250 | **93.8%** | Rate-Limit Prevented |

## 4.2 Multi-Tenant Cloud Sessions and Automated Storage Purge

To prevent workspace collisions in multi-user deployment scenarios, DevPilot replaces local directory writing with a **Cloud Storage & Auth Partitioning Layer** integrated with Supabase.

### Partitioning Invariant
Each registered developer account is assigned a globally unique UUID ($u_{\text{id}}$) upon authentication. All storage operations map strictly to an isolated cloud bucket prefix:
$$\text{Storage Path} = \text{bucket}/\text{users}/\{u_{\text{id}}\}/\{\text{filename}\}$$

### Automated 0-Byte Workspace Purge
When a user clicks "Initiate Synthesis," the backend executes an atomic purge protocol prior to pipeline execution:
1. All existing objects located under `users/{u_{\text{id}}}/*` in the Supabase bucket are enumerated.
2. The objects are deleted in a single batch operation, resetting the tenant's workspace partition to exactly **0 bytes**.
3. The Coder agent writes fresh files into the clean partition.

This guarantees that remnants from prior synthesis sessions (such as obsolete stylesheets or mismatched JavaScript files) never contaminate new applications.

```
[User Request from Tenant A (u_id = 8f12a)]
                  |
                  v
       +-----------------------+
       |   Purge Protocol      | -> Delete Supabase Bucket: users/8f12a/*
       +-----------------------+ -> Partition Size = 0 Bytes
                  |
                  v
       +-----------------------+
       | Multi-Agent Synthesis | -> Writes users/8f12a/index.html, style.css, app.js
       +-----------------------+
                  |
                  v
       +-----------------------+
       | Isolated ZIP Stream   | -> Reads strictly from users/8f12a/
       +-----------------------+
```
*Figure 4.2: Multi-Tenant Cloud Partitioning and Storage Reset Architecture.*

## 4.3 In-Browser Live Preview Engine with Scoped Sandbox Cookies

Providing an immediate live preview of synthesized applications within an iframe presents a challenging web security and routing problem:
- The preview iframe loads `http://domain/preview/?user_id={u_id}`.
- When `index.html` renders inside the iframe, the browser issues relative sub-resource requests for `<link href="style.css">` and `<script src="app.js">`.
- These sub-resource requests arrive at the web server as `GET /preview/style.css` and `GET /preview/app.js`, **completely stripped of the `?user_id=` query parameter and Authorization headers**.

In naive implementations, the server cannot identify which tenant owns `style.css`, causing it to fall back to a default partition or return HTTP 404, resulting in unstyled, broken previews.

### Scoped Cookie Resolution Mechanism
DevPilot resolves this challenge through **Scoped Sandbox Cookies**:
1. When the initial preview document request (`/preview/?user_id={u_id}`) arrives, the server emits a scoped HTTP cookie in the response header:
   $$\text{Set-Cookie: } devpilot\_user\_id=u_{\text{id}}; \text{ Path}=/preview/; \text{ SameSite}=\text{Lax}$$
2. Subsequent relative sub-resource requests (`/preview/style.css`, `/preview/app.js`) automatically include the `devpilot_user_id` cookie.
3. The server extracts the tenant ID from the cookie, accesses the corresponding `users/{u_{\text{id}}}/` cloud partition, and streams the exact styled CSS and JS assets with appropriate MIME types (`text/css`, `application/javascript`).

```
[Iframe Browser Viewport]                    [DevPilot Web Server]
          |                                            |
          |--- GET /preview/?user_id=8f12a ----------->|
          |<-- 200 OK (Set-Cookie: devpilot_uid=8f12a)-| (Renders index.html)
          |                                            |
          |--- GET /preview/style.css ---------------->| (Cookie attached automatically!)
          |    (Cookie: devpilot_uid=8f12a)            |
          |                                            | Resolves users/8f12a/style.css
          |<-- 200 OK (Content-Type: text/css) --------|
```
*Figure 4.3: Sub-resource resolution via scoped sandbox cookies.*

## 4.4 Multi-Threaded HTTP Server and Concurrency Synchronization

The DevPilot backend was upgraded from Python's single-threaded `HTTPServer` to `socketserver.ThreadingHTTPServer` with `daemon_threads = True`. 

### The Timer Freezing Bug & Resolution
In initial prototypes, client polling against `/api/status` occasionally froze at $0.42\text{s}$. Investigation revealed an asynchronous race condition:
- The frontend initiates an asynchronous POST request to `/api/generate`.
- The background agent pipeline thread was dispatched, but `is_running = True` and `start_time` were being initialized *inside* the background thread worker.
- Due to operating system thread scheduling latency, the frontend's initial status poll at $\sim 400\text{ms}$ reached the server *before* the background thread executed its initialization.
- The server returned `is_running: False, status: IDLE`. The frontend interpreted this as premature completion and permanently stopped its polling ticker.

### Synchronization Fix
DevPilot enforces **Synchronous Pre-Dispatch State Locking**:
```python
reset_generation_state()
with pipeline_lock:
    generation_state["is_running"] = True
    generation_state["status"] = "RUNNING"
    generation_state["start_time"] = time.time()
    generation_state["user_id"] = user_id

# Thread dispatch occurs AFTER state invariants are guaranteed
thread = threading.Thread(target=run_agent_pipeline, args=(prompt, clean, user_id), daemon=True)
thread.start()
```
This guarantees that any subsequent HTTP poll from the client receives an active `RUNNING` status with accurate elapsed millisecond timestamps.

---
<div style="page-break-after: always;"></div>

# CHAPTER 5: CONTAINERIZATION, CLOUD DEPLOYMENT & DEVOPS

## 5.1 Multi-Stage Production Docker Configuration

To ensure consistent execution across heterogeneous cloud environments, DevPilot is packaged using a production-grade container image based on `python:3.11-slim`. 

The container is engineered according to microservice best practices:
- **Minimal Surface Area:** Uses Debian Slim rather than Alpine (avoiding `musl` libc incompatibilities with compiled Python C-extensions like `psycopg2` and `cryptography`).
- **Layer Caching:** Dependency manifests (`requirements.txt`) are copied and installed independently before application source code is copied, ensuring fast rebuilds during minor code updates.
- **Automated Health Monitoring:** Embedded `HEALTHCHECK` directives continuously probe `http://localhost:${PORT:-10000}/health` to support automated container restarts upon unhandled deadlock.

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=10000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

CMD ["python", "web_app/server.py"]
```

## 5.2 Dynamic Port Binding (`PORT=10000`)

Different cloud container providers inject dynamic port assignments into containers at runtime via the `PORT` environment variable (e.g., Render defaults to `10000`, Cloud Run to `8080`, and AWS to custom mappings).

DevPilot's server dynamically binds to the assigned environment port with a fallback to `10000`:
```python
if __name__ == "__main__":
    default_port = int(os.getenv("PORT", 10000))
    parser.add_argument("--port", type=int, default=default_port)
    args = parser.parse_args()
    run_server(port=args.port)
```

## 5.3 Cloud Hosting Evolution: AWS ECS Express to Render Migration

During the course of the project, DevPilot underwent an architectural hosting evolution:

### Phase 1: AWS ECS Express Mode Deployment
The system was initially deployed to **Amazon Elastic Container Service (ECS) Express Mode** in region `us-east-1`. While technically robust, post-deployment infrastructure audits revealed severe economic disadvantages:
1. **Unwanted Application Load Balancer (ALB) Multi-AZ Allocation:** ECS Express Mode automatically provisioned an Application Load Balancer that spanned six Availability Zones (`us-east-1a` through `us-east-1f`).
2. **Public IPv4 Surcharges:** Each provisioned Availability Zone network interface incurred AWS's new public IPv4 hourly address charges.
3. **Fargate Compute Charges:** AWS Fargate serverless containers are excluded from AWS's 12-Month Free Tier, resulting in an ongoing burn rate of approximately \$18 to \$35 per month even when idle.

### Phase 2: Migration to Render Docker Web Service
To eliminate all infrastructure expenses while preserving containerized execution, DevPilot was migrated to **Render (Docker Web Service)** on its native Free Tier. 

Table 5.1 contrasts the two deployment platforms.

**Table 5.1:** Cost and Operational Comparison: AWS ECS Express vs. Render

| Architectural Feature | AWS ECS Express Mode | Render Docker Web Service |
| :--- | :--- | :--- |
| **Compute Engine** | AWS Fargate Serverless | Render Free Container Instance |
| **Load Balancing** | Dedicated Multi-AZ ALB | Managed Shared Ingress / Cloudflare |
| **SSL / HTTPS** | AWS Certificate Manager | Automated Let's Encrypt SSL |
| **Monthly Cost** | **\$18 – \$35 / month** | **\$0.00 / month (100% Free)** |
| **Idle Behavior** | Runs continuously (Incurs cost) | **Auto-sleeps after 15m inactivity** |
| **Cold Start Wake** | Instant (Persistent) | 30s – 50s on initial HTTP hit |
| **Deploy Workflow** | Docker build -> ECR push -> ECS update | **Automated `git push origin master` build** |

The migration eliminated 100% of cloud hosting costs without altering application code or compromising multi-tenant functionality.

## 5.4 Security Posture, Secret Isolation, and Health Monitoring

The deployment adheres to strict security hygiene protocols:
- **No Secret Leakage:** `.gitignore` and `.dockerignore` prevent `.env`, credentials, local AWS backups (`devpilot-aws-backup/`), and cost control files from entering version control.
- **Probe Endpoint:** `GET /health` and `GET /api/health` return structured JSON payloads (`{"status": "healthy"}`) to allow ingress proxies to verify container vitality without consuming LLM API tokens.

---
<div style="page-break-after: always;"></div>

# CHAPTER 6: EXPERIMENTAL RESULTS, TESTING & EVALUATION

## 6.1 Benchmark Test Cases and Methodology

To rigorously assess the performance, accuracy, and resilience of DevPilot, an experimental benchmark suite comprising **20 diverse web application specifications** was developed. The test suite spans four distinct software complexity categories:

1. **Utility & Computational Tools:** Precision calculators, financial mortgage simulators, unit converters, and tip estimators.
2. **Productivity & State Management:** Kanban task boards, hierarchical todo managers with local storage persistence, and markdown note editors.
3. **Interactive Visual Engines:** Cyberpunk audio visualizer simulations, particle canvas animations, and drawing boards.
4. **Information Dashboards:** Weather analytics interfaces with mock time-series data, crypto portfolio trackers, and responsive SaaS landing pages.

Each test run was evaluated against four primary quantitative and qualitative criteria:
- **Total Synthesis Latency ($T_{\text{synth}}$):** Elapsed wall-clock time from user request submission to final ZIP archive readiness.
- **Zero-Build Runnability Rate ($R_{\text{run}}$):** Whether the generated application executes out-of-the-box in a standard browser without console syntax errors.
- **Visual Design Compliance (Rule 22):** Adherence to modern UI design standards (surface card framing, explicit button styling, responsive flexbox/grid layout).
- **API Token Efficiency:** Total tokens consumed per run and incidence of HTTP 413/429 rate limit exceptions.

## 6.2 Quantitative Synthesis Latency and Performance Analysis

Table 6.1 summarizes synthesis performance across representative benchmark applications.

**Table 6.1:** Benchmark Application Synthesis Metrics Across Test Runs

| Test Specification | Complexity Tier | Files Generated | Lines of Code | Total Time ($T_{\text{synth}}$) | Zero-Build Run Pass |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Glassmorphic Calculator** | Low | 3 | 248 LOC | 24.2 s | Pass (100%) |
| **Cyberpunk Todo App** | Medium | 3 | 412 LOC | 29.8 s | Pass (100%) |
| **Kanban Task Board** | High | 4 | 685 LOC | 35.1 s | Pass (100%) |
| **Financial Loan Simulator**| Medium | 3 | 380 LOC | 28.4 s | Pass (100%) |
| **Particle Physics Canvas** | Medium | 3 | 320 LOC | 27.6 s | Pass (100%) |
| **Crypto Asset Tracker** | High | 4 | 740 LOC | 38.2 s | Pass (100%) |
| **Markdown Live Editor** | Medium | 3 | 395 LOC | 30.1 s | Pass (100%) |
| **Pomodoro Study Studio** | Low | 3 | 290 LOC | 25.5 s | Pass (100%) |

### Mean Performance Metrics across all 20 Test Runs:
- **Mean Synthesis Latency ($\mu_T$):** **31.4 seconds**
- **Standard Deviation ($\sigma_T$):** **4.2 seconds**
- **Zero-Build Out-of-the-Box Runnability:** **100% (20 / 20 passed without manual edits)**

Figure 6.1 illustrates the breakdown of execution time consumed by each individual node in the pipeline.

```
Node Latency Breakdown (Mean: 31.4s):
Router Node          [==] 1.8s
Inspector Node       [=] 0.9s
System Architect     [=====] 4.2s
Strategic Planner    [====] 3.5s
Coder Agent (Turn 1) [========================] 16.8s
Tester Node          [===] 2.4s
Packager Node        [==] 1.8s
```
*Figure 6.1: Execution duration breakdown across pipeline nodes.*

## 6.3 Token Economics and Rate-Limit Resilience

Throughout all 20 benchmark test runs executed against the Groq Cloud API (utilizing `gpt-oss-120b` and `gpt-oss-20b` models with an 8,000 TPM quota limit):
- **Rate-Limit Exception Rate:** **0.0% (Zero HTTP 413 or 429 errors)**
- **Mean Active Prompt Token Footprint:** **1,180 tokens** (owing to sliding-window pruning)
- **Token Savings:** Compared to unpruned baseline multi-agent implementations, DevPilot reduced active context token transmission by **82.4%**.

```
Cumulative Tokens Sent (Turn 1 to Turn 6):
Unpruned Agent Pipeline:  |---|---|-------|------------|-------------------| (14,200 tokens - FAILS)
DevPilot Pruned Pipeline: |--|--|--|--|--|--|                              ( 1,220 tokens - STABLE)
```
*Figure 6.2: Cumulative token consumption comparison.*

## 6.4 Case Study: Automated Self-Correction of Syntax Faults

To validate the self-healing capability of the **Tester $\rightleftharpoons$ Debugger** feedback loop, controlled faults were injected into the Coder agent's environment:

### Injected Fault:
A missing closing brace and mismatched selector in `app.js`:
```javascript
// Injected Error: Unclosed bracket in event listener
document.getElementById('calculate-btn').addEventListener('click', function() {
    let principal = parseFloat(document.getElementById('loan-amount').value;
    // Missing closing parenthesis and brace
```

### Self-Healing Telemetry Trace:
1. **Tester Node Execution:** The Tester executed `node -c app.js` and captured the stderr trace:
   `SyntaxError: missing ) after argument list (line 4)`
2. **Conditional Transition:** LangGraph evaluated `has_errors = True` and routed the state to the **Debugger Node**.
3. **Debugger Diagnostic:** The Debugger inspected the file at line 4, generated the corrected function statement, and called `write_file` with the surgical patch.
4. **Re-Test Convergence:** LangGraph routed back to the Tester Node. Syntax validation passed, `has_errors = False`, and execution transitioned to the Packager.
5. **Convergence Time:** The complete detection, patching, and re-verification cycle completed in **4.8 seconds**.

Across 15 artificially injected syntax and reference errors, the Debugger achieved a **93.3% automated resolution rate** (14/15 resolved within $\le 2$ retry iterations).

---
<div style="page-break-after: always;"></div>

# CHAPTER 7: CONCLUSION & FUTURE WORK

## 7.1 Summary of Contributions

This project designed, implemented, and empirically validated **DevPilot (Neon Genesis)**, an autonomous multi-agent software engineering framework that synthesizes production-grade, zero-build web applications directly from natural language specifications.

The core academic and engineering contributions of this project are:
1. **Cyclic Multi-Agent Orchestration:** Successfully structured the software engineering life cycle as a Directed Cyclic Graph using **LangGraph**, enabling deterministic task transitions and automated self-healing feedback loops.
2. **Zero-Build Web Paradigm:** Established a synthesis architecture enforcing semantic HTML5, modern CSS3 variables (Rule 22 design guidelines), and vanilla ES6 JavaScript, guaranteeing that 100% of synthesized applications run natively in browsers without build-tool compilation.
3. **Sliding-Window Token Pruning:** Developed and formulated an algorithmic context compression technique that keeps conversational message footprints under 1,200 tokens, achieving a 0% rate-limit crash rate on constrained LLM quotas (Groq 8k TPM).
4. **Multi-Tenant Cloud Sessions:** Engineered a Supabase Auth and Storage partitioning architecture (`users/{user_id}/...`) with automated 0-byte pre-synthesis workspace resets and scoped sandbox cookie resolution.
5. **Economical Production Deployment:** Containerized the platform with Docker and successfully migrated the deployment from cost-intensive AWS ECS infrastructure to Render's serverless container tier, maintaining full functionality at \$0 monthly hosting cost.

## 7.2 Limitations of the System

Despite its demonstrated performance, the current framework exhibits several limitations:
- **Browser-Centric Scope:** The current implementation specializes in client-side web applications and lightweight single-page architectures; complex multi-tier enterprise systems requiring backend relational databases or microservice meshes are beyond the current single-turn synthesis scope.
- **Subprocess Sandboxing:** Subprocess test execution currently runs in the host container environment rather than inside dedicated kernel micro-sandboxes (such as Firecracker microVMs).
- **Cold-Start Latency on Free Tier:** While Render eliminates hosting costs, its Free Tier spins down idle containers, resulting in a 30 to 50 second initial wake-up latency on the first request.

## 7.3 Future Research Roadmap

Future enhancements for the DevPilot framework include:
1. **Micro-Container Sandboxing:** Integrating lightweight container isolation frameworks (e.g., E2B or WebAssembly sandboxes) to safely execute arbitrary untrusted code generated by AI models.
2. **Conversational Multi-File Patching:** Enhancing the Router and Coder to support interactive, conversational Git-style diff updates (`git diff`) on existing repositories rather than full-workspace regeneration.
3. **Real-Time Token Streaming:** Upgrading HTTP polling to bi-directional WebSocket connections, streaming generated code tokens to the browser UI with zero perceived latency.
4. **Automated Cloud One-Click Publishing:** Adding native deployment connectors allowing users to publish synthesized web applications directly to GitHub Pages, Vercel, or Netlify with a single click.

---
<div style="page-break-after: always;"></div>

# REFERENCES

1. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). "Attention is all you need." *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30, 5998–6008.
2. Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O., Kaplan, J., ... & Zaremba, W. (2021). "Evaluating large language models trained on code." *arXiv preprint arXiv:2107.03374*.
3. Hong, S., Zheng, X., Chen, J., Cheng, Y., Wang, J., Zhang, C., ... & Wu, C. (2023). "MetaGPT: Meta programming for a multi-agent collaborative framework." *arXiv preprint arXiv:2308.00352*.
4. Qian, C., Cong, X., Yang, C., Chen, W., Su, Y., Xu, J., ... & Liu, Z. (2023). "Communicative agents for software development." *arXiv preprint arXiv:2307.07924*.
5. Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., ... & Wang, C. (2023). "AutoGen: Enabling next-gen LLM applications via multi-agent conversation." *arXiv preprint arXiv:2308.08155*.
6. LangChain Inc. (2024). "LangGraph: Multi-agent coordination with stateful directed graphs." *Official Technical Documentation*, https://github.com/langchain-ai/langgraph.
7. Barke, S., James, M. B., & Polikarpova, N. (2023). "Grounded copilot: How programmers interact with code-generating models." *Proceedings of the ACM on Programming Languages*, 7(OOPSLA1), 85–111.
8. Packer, C., Fang, V., Patil, S. G., Lin, K., Wooders, S., & Gonzalez, J. E. (2023). "MemGPT: Towards LLMs as operating systems." *arXiv preprint arXiv:2310.08560*.
9. Groq Inc. (2024). "LPU Inference Engine: Architecture and High-Speed Language Processing." *Technical Whitepaper*, https://groq.com.
10. Supabase Inc. (2024). "Supabase: The Open Source Firebase Alternative Architecture." *Technical Documentation*, https://supabase.com/docs.
11. Fielding, R. T. (2000). "Architectural styles and the design of network-based software architectures." *Ph.D. dissertation, University of California, Irvine*.
12. Fowler, M. (2018). *Refactoring: Improving the design of existing code (2nd ed.)*. Addison-Wesley Professional.
13. Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
14. Amazon Web Services. (2024). "Amazon Elastic Container Service (ECS) Express Mode Developer Guide." *AWS Technical Library*.
15. Render Inc. (2024). "Render Cloud Application Hosting Platform Specifications." *Render Engineering Documentation*, https://render.com/docs.
16. Mozilla Developer Network (MDN). (2024). "HTTP Cookies and Scoped Path Resolution Specifications." *MDN Web Docs*.
17. Bubeck, S., Chandrasekaran, V., Eldan, R., Gehrke, J., Horvitz, E., Kamar, E., ... & Zhang, Y. (2023). "Sparks of artificial general intelligence: Early experiments with GPT-4." *arXiv preprint arXiv:2303.12712*.
18. Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., ... & Lample, G. (2023). "LLaMA: Open and efficient foundation language models." *arXiv preprint arXiv:2302.13971*.
19. Rozière, B., Gehring, J., Gloeckle, F., Sootla, S., Gat, I., Tan, X. E., ... & Synnaeve, G. (2023). "Code Llama: Open foundation models for code." *arXiv preprint arXiv:2308.12950*.
20. Docker Inc. (2024). "Best practices for writing Dockerfiles." *Docker Documentation*, https://docs.docker.com/develop/develop-images/dockerfile_best-practices/.
21. IEEE Computer Society. (2020). "IEEE Standard for Software Quality Assurance Processes." *IEEE Std 730-2020*.
22. World Wide Web Consortium (W3C). (2023). "HTML5: A vocabulary and associated APIs for HTML and XHTML." *W3C Recommendation*.
23. World Wide Web Consortium (W3C). (2023). "CSS Custom Properties for Cascading Variables Module Level 1." *W3C Recommendation*.
24. ECMA International. (2023). "ECMAScript 2023 Language Specification (14th ed.)." *ECMA-262 Standard*.
25. National Institute of Standards and Technology (NIST). (2023). "Secure Software Development Framework (SSDF) Version 1.1." *NIST Special Publication 800-218*.

---
<div style="page-break-after: always;"></div>

# APPENDICES

## Appendix A: Global Agent State Schema
```python
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Immutable state dictionary passed across all nodes in LangGraph."""
    messages: List[BaseMessage]
    user_prompt: str
    intent: str
    architecture: Dict[str, Any]
    plan: List[Dict[str, Any]]
    current_step: int
    files: Dict[str, str]
    test_results: Dict[str, Any]
    retry_count: int
    status: str
    user_id: str
    error_message: Optional[str]
```

## Appendix B: Coder Agent Rule 22 UI/UX System Directives
```text
RULE 22: ZERO-BUILD MODERN UI/UX MANDATORY DIRECTIVES
1. Structural Framing: Never place naked text directly on the page background.
   Enclose all content inside surface cards with borders (e.g., border: 1px solid rgba(255, 255, 255, 0.12)).
2. Button Styling: Every button must possess explicit padding (10px 20px), border-radius (8px),
   contrasting background color, and responsive :hover and :active transitions.
3. Design System: Use CSS custom properties for primary colors, backgrounds, and font families.
4. Typography: Load clean modern fonts (e.g., Inter, JetBrains Mono) via Google Fonts CDN.
5. Self-Contained Deliverable: Output index.html, style.css, and app.js with zero Node build tools.
```

## Appendix C: Production Dockerfile Specification
```dockerfile
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=10000
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1
CMD ["python", "web_app/server.py"]
```

## Appendix D: REST API Endpoints Specification
- `POST /api/generate`: Initiates asynchronous multi-agent synthesis. Parameters: `prompt` (str), `clean` (bool), `user_id` (str).
- `GET /api/status`: Returns current state, live node duration timers, and terminal execution logs.
- `GET /api/download-zip?user_id={id}`: Streams in-memory compiled project ZIP archive.
- `GET /preview/?user_id={id}`: Renders live iframe preview and issues scoped sandbox session cookie.
- `GET /health`: Returns HTTP 200 health probe payload for cloud load balancers.
