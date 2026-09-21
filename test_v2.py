from agents_v2.graph import app


requests = [
    "Build me a todo application",
    "Add dark mode to my existing React app",
    "My login button crashes when I click it",
    "Run tests on my project",
    "Explain how authentication works",
    "Hello!",
]


for request in requests:
    result = app.invoke(
        {
            "user_request": request,
            "iteration": 0,
            "status": "STARTING",
            "errors": [],
            "files_changed": [],
            "tasks": [],
        }
    )

    print("\n" + "=" * 70)
    print("Request :", request)
    print("Intent  :", result["intent"])
    print("Status  :", result["status"])

    if result.get("plan"):
        print("\nGOAL:")
        print(result["plan"]["goal"])

        print("\nAPPROACH:")
        print(result["plan"]["approach"])

        print("\nTASKS:")

        for task in result["tasks"]:
            print(
                f"\n[{task['id']}] {task['description']}"
            )
            print(f"    Files: {task['files']}")
            print(f"    Why:   {task['reasoning']}")

        print("\nCONSTRAINTS:")

        for constraint in result["plan"]["constraints"]:
            print(f"- {constraint}")