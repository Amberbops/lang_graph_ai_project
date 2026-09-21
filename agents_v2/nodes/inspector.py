from pathlib import Path
import json

from agents_v2.models import get_fast_model
from agents_v2.states import AgentState
from tools.project.workspace import PROJECT_ROOT
from tools.filesystem.operations import list_files


def detect_project_type() -> str:
    """
    Detect the likely project framework/type from common files.
    """

    root = Path(PROJECT_ROOT)

    if (root / "package.json").exists():
        try:
            package_data = json.loads(
                (root / "package.json").read_text(encoding="utf-8")
            )

            dependencies = {
                **package_data.get("dependencies", {}),
                **package_data.get("devDependencies", {}),
            }

            if "next" in dependencies:
                return "Next.js"

            if "react" in dependencies:
                return "React"

            if "vue" in dependencies:
                return "Vue"

            if "express" in dependencies:
                return "Node.js / Express"

            return "Node.js"

        except (json.JSONDecodeError, OSError):
            return "Node.js"

    if (root / "requirements.txt").exists():
        return "Python"

    if (root / "pyproject.toml").exists():
        return "Python"

    if (root / "manage.py").exists():
        return "Django"

    return "Unknown"


def inspector_node(state: AgentState) -> AgentState:
    """
    Inspect the current project workspace.
    """

    project_files = list_files.invoke(
        {"directory": "."}
    )

    project_type = detect_project_type()

    # Keep the initial version simple.
    # The LLM will later turn this raw information into
    # a more detailed project understanding.
    model = get_fast_model()

    response = model.invoke(
        f"""
You are a software project inspector.

Analyze the following project information.

Project type:
{project_type}

Files:
{project_files}

Return a concise project summary containing:

1. Project type/framework
2. Main technologies
3. Important files
4. Likely entry point
5. Any obvious missing or suspicious files

Do not modify any files.
"""
    )

    project_structure = response.content

    return {
        **state,
        "project_structure": project_structure,
        "status": "INSPECTED",
    }