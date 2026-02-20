import asyncio
from datetime import datetime

import db


def add_tool(title: str, description: str = "") -> dict:
    """
    Adds a new task to the task list
    """
    created_at = datetime.now().isoformat()
    return asyncio.run(db.insert_task(title, description, created_at))


def complete_task(task_id: int) -> dict:
    """
    Marks a task as completed
    """
    completed_at = datetime.now().isoformat()
    result = asyncio.run(db.update_task_status(task_id, "completed", completed_at))
    if result is None:
        return {"error": f"Task {task_id} not found"}
    return result

def delete_task(task_id: int) -> dict:
    """
    Deletes a task
    """
    deleted = asyncio.run(db.remove_task(task_id))
    if deleted is None:
        return {"success": False, "error": f"Task {task_id} not found"}
    return {"success": True, "deleted": deleted}