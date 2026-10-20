"""
Generate a professional, publication-quality PDF synopsis for DevPilot.
Uses ReportLab Platypus with custom styles, tables, and page numbering.
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.pdfgen import canvas

# Output Path
ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_PDF = ROOT_DIR / "SYNOPSIS.pdf"


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total pages and draw footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "DevPilot — Autonomous Agentic Software Engineering System (Synopsis)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — DevPilot Engineering Group | ambersaluja20006@gmail.com")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)

        self.restoreState()


def build_pdf(output_path: Path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Slate / Navy
    SECONDARY = colors.HexColor("#2563EB")  # Electric Blue
    ACCENT = colors.HexColor("#0284C7")     # Sky Blue
    DARK_TEXT = colors.HexColor("#1E293B")  # Charcoal body
    MUTED_TEXT = colors.HexColor("#64748B") # Muted grey
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Light background
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=14,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6,
    )

    body_bold = ParagraphStyle(
        "Body_Bold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=DARK_TEXT,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=PRIMARY,
    )

    story = []

    # =========================================================================
    # Header Banner & Metadata Block
    # =========================================================================
    story.append(Paragraph("DEVPILOT: AUTONOMOUS AGENTIC SOFTWARE ENGINEERING SYSTEM", title_style))
    story.append(Paragraph("System Architecture, Multi-Agent Orchestration & Production Deployment Synopsis", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    meta_data = [
        [
            Paragraph("<b>Project:</b> DevPilot (Agents v2)", body_style),
            Paragraph("<b>Core Frameworks:</b> LangGraph, LangChain, Groq, Gemini", body_style),
        ],
        [
            Paragraph("<b>Author / Owner:</b> ambersaluja20006@gmail.com", body_style),
            Paragraph("<b>Security & Storage:</b> Supabase Auth & Cloud Partitions", body_style),
        ],
        [
            Paragraph("<b>Repository:</b> lang_graph_ai_project (master)", body_style),
            Paragraph("<b>Deployment Target:</b> AWS Amplify / App Runner / Docker", body_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[240, 264])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 1. Executive Summary
    # =========================================================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>DevPilot</b> is an autonomous, multi-agent AI software engineering framework designed to convert natural language "
        "prompts into complete, fully functional, zero-build software applications delivered as standalone packages. "
        "Unlike conventional LLM code assistants that output disconnected snippets requiring manual developer compilation, "
        "DevPilot manages an end-to-end <b>Agentic Software Development Life Cycle (SDLC)</b>.",
        body_style,
    ))
    story.append(Paragraph(
        "Powered by <b>LangGraph</b>, DevPilot structures AI reasoning into a cyclic, stateful directed graph. The system autonomously "
        "classifies intent, inspects project environments, formulates modular architectures, coordinates parallel code generation, "
        "validates functionality via test runners, and executes automated self-healing loops when syntax or logic errors occur. "
        "Every completed application is rendered in a live sandbox preview and packaged into an instant, zero-build ZIP archive.",
        body_style,
    ))

    # =========================================================================
    # 2. Key Problem Statements & Core Solutions
    # =========================================================================
    story.append(Paragraph("2. Problems Addressed & Engineering Solutions", h1_style))
    problems_data = [
        [
            Paragraph("Traditional Challenge", table_header_style),
            Paragraph("DevPilot Engineering Solution", table_header_style),
        ],
        [
            Paragraph("<b>Context Fragmentation:</b> LLMs generate isolated files that fail to integrate, miss CSS styling, or omit entry points.", table_cell_style),
            Paragraph("<b>Stateful LangGraph Memory:</b> Global state synchronizes architectural models and task definitions across every specialized agent node.", table_cell_style),
        ],
        [
            Paragraph("<b>Rate Limit (TPM) Exhaustion:</b> Multi-turn agent loops quickly exceed provider ceilings (e.g., Groq 8k TPM).", table_cell_style),
            Paragraph("<b>Sliding-Window Pruning & Batching:</b> Coder emits all core files in Turn 1; messages are pruned to retain low-token context with multi-model failover.", table_cell_style),
        ],
        [
            Paragraph("<b>Over-Engineered Scaffolding:</b> Heavy build tools (Vite/Webpack) break during compilation without human intervention.", table_cell_style),
            Paragraph("<b>Zero-Build Standalone Architecture:</b> Native HTML5, modern CSS3 variables, and vanilla ES6 run directly in any browser out of the box.", table_cell_style),
        ],
        [
            Paragraph("<b>Multi-User Data Collisions:</b> Shared workspaces cause concurrent user requests to overwrite each other's files.", table_cell_style),
            Paragraph("<b>Isolated Cloud Partitions:</b> Supabase Auth partitions storage under <code>users/{user_id}/</code>, resetting workspace to 0 bytes on each synthesis.", table_cell_style),
        ],
    ]
    prob_table = Table(problems_data, colWidths=[240, 264])
    prob_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. Directed Multi-Agent Graph Architecture
    # =========================================================================
    story.append(Paragraph("3. Multi-Agent Pipeline Architecture (Agents v2)", h1_style))
    story.append(Paragraph(
        "DevPilot models software synthesis through specialized, communicating agent personas organized in a LangGraph <code>StateGraph</code>:",
        body_style,
    ))

    agents_data = [
        [
            Paragraph("Agent Node", table_header_style),
            Paragraph("Role & Specialization", table_header_style),
            Paragraph("Core Model & Mechanism", table_header_style),
        ],
        [
            Paragraph("<b>🧭 Router</b>", table_cell_bold),
            Paragraph("Analyzes user prompts; routes to CREATE, MODIFY, DEBUG, TEST, or CHAT intent.", table_cell_style),
            Paragraph("Gemini Flash-Lite / Groq Auto", table_cell_style),
        ],
        [
            Paragraph("<b>🔍 Inspector</b>", table_cell_bold),
            Paragraph("Audits filesystem, languages, dependencies, and project manifests.", table_cell_style),
            Paragraph("Sandboxed Filesystem Tools", table_cell_style),
        ],
        [
            Paragraph("<b>📐 Architect</b>", table_cell_bold),
            Paragraph("Designs component layout, data flow, tech stack, and zero-build rules.", table_cell_style),
            Paragraph("Groq GPT-OSS 120B (Structured)", table_cell_style),
        ],
        [
            Paragraph("<b>📋 Planner</b>", table_cell_bold),
            Paragraph("Deconstructs architecture into 4–7 prioritized, sequential tasks.", table_cell_style),
            Paragraph("Groq GPT-OSS 120B (Pydantic)", table_cell_style),
        ],
        [
            Paragraph("<b>⚡ Coder</b>", table_cell_bold),
            Paragraph("Batch-writes source code, modern CSS design systems, and responsive logic.", table_cell_style),
            Paragraph("Groq Tool-Calling + Rule 22 UI", table_cell_style),
        ],
        [
            Paragraph("<b>🧪 Tester</b>", table_cell_bold),
            Paragraph("Discovers unit tests, executes test commands, and parses stdout/stderr.", table_cell_style),
            Paragraph("Subprocess Runner + LLM Parser", table_cell_style),
        ],
        [
            Paragraph("<b>🛠️ Debugger</b>", table_cell_bold),
            Paragraph("Investigates test failures and applies surgical fixes in an automated loop.", table_cell_style),
            Paragraph("Groq Reasoning Agent (Max 6x)", table_cell_style),
        ],
        [
            Paragraph("<b>📦 Packager</b>", table_cell_bold),
            Paragraph("Compresses user workspace directly from Supabase Storage into ZIP.", table_cell_style),
            Paragraph("Python in-memory <code>zipfile</code>", table_cell_style),
        ],
    ]
    agent_table = Table(agents_data, colWidths=[90, 240, 174])
    agent_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(agent_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. Technical Innovations & System Upgrades
    # =========================================================================
    story.append(Paragraph("4. Technical Innovations & Production Upgrades", h1_style))
    
    story.append(Paragraph("<b>A. Authentication Gateway & Session Isolation:</b>", body_bold))
    story.append(Paragraph(
        "• <b>Enforced Auth Gateway:</b> Unauthenticated visitors attempting to open <code>/app</code> are instantly intercepted "
        "and redirected to <code>/login</code> via an inline <code>&lt;head&gt;</code> guard with zero content flash.<br/>"
        "• <b>Supabase Cloud Partitions:</b> Every registered account is granted an isolated storage bucket prefix (<code>users/{user_id}/</code>). "
        "On every new prompt, the user's partition is cleanly purged to 0 bytes before generation, ensuring zero cross-run pollution.",
        bullet_style,
    ))

    story.append(Paragraph("<b>B. In-Browser Live Preview & Dynamic Sandbox Cookies:</b>", body_bold))
    story.append(Paragraph(
        "• <b>Sub-Resource Scoped Cookies:</b> Preview requests issue a scoped <code>Set-Cookie: devpilot_user_id={user_id}; Path=/preview/</code> header. "
        "This ensures that relative sub-resource requests (such as <code>style.css</code> or <code>app.js</code> loaded by the iframe) "
        "always resolve to the specific user's generated partition instead of falling back to default.<br/>"
        "• <b>Device Emulation:</b> Studio dashboard features one-click viewport toggles (Desktop vs. Mobile 375px) and external window launch.",
        bullet_style,
    ))

    story.append(Paragraph("<b>C. Concurrency & Real-Time Antigravity Timers:</b>", body_bold))
    story.append(Paragraph(
        "• <b>ThreadingHTTPServer:</b> Upgraded web server from single-threaded to <code>ThreadingHTTPServer</code> with daemon threads, "
        "eliminating socket starvation and blocking during background agent pipeline execution.<br/>"
        "• <b>Atomic State Initialization:</b> Server synchronizes <code>is_running = True</code> and <code>start_time</code> before thread dispatch, "
        "eliminating early poll race conditions and preventing timer freezes.",
        bullet_style,
    ))

    # =========================================================================
    # 5. Deployment Architecture & Production Readiness
    # =========================================================================
    story.append(Paragraph("5. Cloud Deployment & Containerization Readiness", h1_style))
    deploy_items = [
        "<b>Dockerfile:</b> Multi-stage, production Python 3.11-slim container with automatic non-root execution and dynamic <code>$PORT</code> binding.",
        "<b>Health Probes:</b> Verified <code>GET /health</code> and <code>GET /api/health</code> endpoints returning HTTP 200 JSON payloads for ALB/Amplify probes.",
        "<b>AWS Amplify Build Spec:</b> <code>amplify.yml</code> pre-configured with caching and container launch scripts.",
        "<b>Strict Credential Isolation:</b> <code>.gitignore</code> and <code>.env.example</code> verify that no API keys or database tokens can leak into version control.",
    ]
    for item in deploy_items:
        story.append(Paragraph(f"• {item}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 6. Conclusion & Operational Status
    # =========================================================================
    story.append(Paragraph("6. Project Status & Summary", h1_style))
    story.append(Paragraph(
        "DevPilot has achieved stable, production-grade maturity. All automated SDLC stages—from intent extraction to cloud ZIP export—"
        "operate reliably with verified sub-35 second synthesis times. The repository is fully staged, tested, and ready for deployment.",
        body_style,
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")


if __name__ == "__main__":
    build_pdf(OUTPUT_PDF)
