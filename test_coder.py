from agents_v2.graph import app


request = "Add a dark mode toggle to my existing application."

result = app.invoke(
    {
        "user_request": request,
        "iteration": 0,
        "status": "STARTING",
        "messages": [],
        "errors": [],
        "files_changed": [],
        "tasks": [],
    }
)

print("\n" + "=" * 70)
print("REQUEST:")
print(request)

print("\nINTENT:")
print(result.get("intent"))

print("\nSTATUS:")
print(result.get("status"))

print("\nTOOL CALLS:")
print(
    result.get("current_task", {}).get(
        "tool_calls",
        []
    )
)

print("\nFILES CHANGED:")
print(result.get("files_changed", []))

print("\nFINAL MESSAGE:")
messages = result.get("messages", [])

if messages:
    print(messages[-1].content)
else:
    print("No messages.")