from datetime import datetime

from task_server import mcp
from tools import tasks, task_id_counter


@mcp.resource("tasks://all")
def get_all_tasks() -> str:
    """
        Gets all tasks as formatted text
    """
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