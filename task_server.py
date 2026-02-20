from fastmcp import FastMCP

mcp = FastMCP("TaskTracker")

import resources.resources  # noqa: E402, F401
import tools.tools  # noqa: E402, F401


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
