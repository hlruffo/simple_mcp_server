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


@mcp.tool()
def complete_task(task_id: int) -> dict:
    """
        Marks a task as completed
    """
    try:
        for task in tasks:
            if task["id"] == task_id:
                task["status"] == "completed"
                task["completed_at"] == datetime.now().isoformat()
                return task
    except ValueError as nfe:
        raise nfe(f"Task with id {task_id} was not found.")
    except Exception as e:
        raise e("Failed to complete task.")
    

@mcp.tool()
def delete_task(task_id: int) -> dict:
    """
        Deletes a task
    """
    try: 
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted_task = tasks.pop(i)
                return {
                    "success": True, 
                    "deleted": deleted_task,
                }
    except Exception as e:
        raise e("Failed to delete task")