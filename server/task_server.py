import asyncio

from db import init_db
from fastmcp import FastMCP

mcp = FastMCP("TaskTracker")

asyncio.run(init_db())

from resources.resources import get_all_tasks, get_pending_tasks  # noqa: E402
from tools.tools import add_tool, complete_task, delete_task  # noqa: E402

# Register tools
mcp.tool(name="add_task")(add_tool)
mcp.tool()(complete_task)
mcp.tool()(delete_task)

# Register resources
mcp.resource("tasks://all")(get_all_tasks)
mcp.resource("task://pending")(get_pending_tasks)


@mcp.prompt()
def task_summary_prompt() -> str:
    """Generate a prompt for summarizing tasks."""
    return """Please analyze the current task list and provide:

1. Total number of tasks (completed vs pending)
2. Any overdue or high-priority items
3. Suggested next actions
4. Overall progress assessment

Use the tasks://all resource to access the complete task list."""


if __name__ == "__main__":
    mcp.run()
