from datetime import datetime

import sys

mcp = sys.modules["__main__"].mcp

# simple in-memory task storage
tasks = []
task_id_counter = 1


# implementing tools
@mcp.tool()
def add_task(title: str, description: str = "") -> dict:
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


@mcp.tool()
def complete_task(task_id: int) -> dict:
    """
    Marks a task as completed
    """
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
            return task
    return {"error": f"Task {task_id} not found"}


@mcp.tool()
def delete_task(task_id: int) -> dict:
    """
    Deletes a task
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            return {
                "success": True,
                "deleted": deleted_task,
            }
    return {"success": False, "error": f"Task {task_id} not found"}
