import asyncio
from pathlib import Path

from fastmcp import Client

SERVER_PATH = Path(__file__).parent.parent / "server" / "task_server.py"


async def test_server():
    async with Client(SERVER_PATH) as client:
        # get tools
        tools = await client.list_tools()
        print("Available tools are:", [t for t in tools])

        # add task
        result = await client.call_tool(
            "add_task",
            {"title": "Learn MCP", "description": "Build a task tracker with FastMCP"},
        )
        print("\nAdded task:", result.content[0].text)

        # view all tasks
        resources = await client.list_resources()
        print("\nAvailable resources:", [r.uri for r in resources])

        task_list = await client.read_resource("tasks://all")
        print("\nAll tasks:\n", task_list[0].text)


asyncio.run(test_server())
