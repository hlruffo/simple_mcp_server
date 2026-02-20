import asyncio

import db


def get_all_tasks() -> str:
    """
    Gets all tasks as formatted text
    """
    tasks = asyncio.run(db.fetch_all_tasks())

    if not tasks:
        return "No task found"

    result = "Current tasks: \n\n"
    for task in tasks:
        status_emoji = "✅" if task["status"] == "completed" else "⏳"
        result += f"{status_emoji} [{task['id']}] {task['title']} \n"
        if task["description"]:
            result += f"Description: {task['description']}\n"
        result += f"Status: {task['status']}\n"
        result += f"Created: {task['created_at']}\n\n"

    return result


def get_pending_tasks() -> str:
    """
    Returns only pending tasks
    """
    tasks = asyncio.run(db.fetch_all_tasks())
    pending = [t for t in tasks if t["status"] == "pending"]

    if not pending:
        return "No pending tasks! All done! Congrats!"

    result = "Pending Tasks: \n\n"
    for task in pending:
        result += f"⏳ [{task['id']}] {task['title']}\n"
        if task["description"]:
            result += f"   {task['description']}\n"
        result += "\n"

    return result
