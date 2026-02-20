from datetime import datetime

from fastmcp import FastMCP

mcp = FastMCP("TaskTracker")

# simple in-memory task storage
tasks = []
task_id_counter = 1


# implementing tools
@mcp.tool()
def add_tool(title: str, description: str = "") -> dict:
    """
    Adds a new task to the task list
    """
    global task_id_counter

    task = {
        "id": task_id_counter,
        "title": title,
        "description": description,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    tasks.append(task)
    task_id_counter += 1
    return task
