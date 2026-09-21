"""
DevPilot — main entry point.

Usage:
    uv run python main.py

    or with a custom recursion limit:
    uv run python main.py --recursion-limit 150
"""

import argparse
import json
import sys
import traceback

from tools.project.workspace import init_project_root
from agents_v2.graph import app


def main():
    parser = argparse.ArgumentParser(description="DevPilot — AI Software Development Agent")
    parser.add_argument(
        "--recursion-limit", "-r",
        type=int,
        default=150,
        help="LangGraph recursion limit (default: 150).",
    )
    parser.add_argument(
        "--project-path", "-p",
        type=str,
        default="",
        help="Optional path for the generated project workspace.",
    )
    parser.add_argument(
        "--clean", "-c",
        action="store_true",
        help="Clear generated_project workspace before running.",
    )

    args = parser.parse_args()

    clean_requested = args.clean

    try:
        user_request = input("DevPilot › ").strip()

        if not user_request:
            print("No request entered. Exiting.")
            sys.exit(0)

        # Check if user explicitly asked to clear or recreate workspace
        clean_phrases = [
            "clear generated_project",
            "clear the folder",
            "clear folder",
            "clear directory",
            "clear it",
            "clean folder",
            "clean directory",
            "remove existing",
            "delete existing",
            "from scratch",
            "from new",
            "build it from new",
        ]
        if any(phrase in user_request.lower() for phrase in clean_phrases):
            clean_requested = True

        # Initialise the generated project workspace
        init_project_root(clean=clean_requested)
        if clean_requested:
            print("🧹 Cleaned generated_project directory.")


        initial_state = {
            "user_request": user_request,
            "messages": [],
            "errors": [],
            "files_changed": [],
            "tool_calls_count": 0,
            "iteration": 0,
            "debug_iteration": 0,
        }

        print("\n🚀  Running DevPilot agentic chain …\n")

        result = app.invoke(
            initial_state,
            {"recursion_limit": args.recursion_limit},
        )

        # ------------------------------------------------------------------
        # Display results
        # ------------------------------------------------------------------

        print("\n" + "=" * 60)
        print("✅  DevPilot finished")
        print("=" * 60)

        intent = result.get("intent", "UNKNOWN")
        status = result.get("status", "UNKNOWN")
        print(f"Intent  : {intent}")
        print(f"Status  : {status}")

        files_changed = result.get("files_changed", [])
        if files_changed:
            print(f"\nFiles changed ({len(files_changed)}):")
            for f in sorted(set(files_changed)):
                print(f"  • {f}")

        test_results = result.get("test_results")
        if test_results:
            print("\nTest results:")
            passed = test_results.get("passed", 0)
            failed = test_results.get("failed", 0)
            success = test_results.get("success", False)
            icon = "✅" if success else "❌"
            print(f"  {icon} {passed} passed / {failed} failed")
            summary = test_results.get("summary", "")
            if summary:
                print(f"  {summary}")

        errors = result.get("errors", [])
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for err in errors:
                print(f"  ⚠️  {err}")

        plan = result.get("plan")
        if plan and intent != "EXPLAIN":
            print(f"\nGoal: {plan.get('goal', '')}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)

    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()