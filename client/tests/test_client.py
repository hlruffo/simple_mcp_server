import pytest

import tools.tools as tools_module
from fastmcp import Client, FastMCP
from resources.resources import get_all_tasks, get_pending_tasks
from tools.tools import add_tool, complete_task, delete_task


@pytest.fixture
def mcp_server():
    """Create a fresh FastMCP server with all tools and resources registered."""
    mcp = FastMCP("TaskTracker")
    mcp.tool(name="add_task")(add_tool)
    mcp.tool()(complete_task)
    mcp.tool()(delete_task)
    mcp.resource("tasks://all")(get_all_tasks)
    mcp.resource("task://pending")(get_pending_tasks)
    return mcp


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory state before each test."""
    tools_module.tasks.clear()
    tools_module.task_id_counter = 1
    yield
    tools_module.tasks.clear()
    tools_module.task_id_counter = 1


# ---------------------------------------------------------------------------
# list_tools
# ---------------------------------------------------------------------------


class TestListTools:
    @pytest.mark.anyio
    async def test_lista_ferramentas_disponiveis(self, mcp_server):
        async with Client(mcp_server) as client:
            tools = await client.list_tools()
            names = {t.name for t in tools}
            assert "add_task" in names
            assert "complete_task" in names
            assert "delete_task" in names


# ---------------------------------------------------------------------------
# add_task
# ---------------------------------------------------------------------------


class TestAddTask:
    @pytest.mark.anyio
    async def test_retorna_task_criada(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool(
                "add_task",
                {"title": "Learn MCP", "description": "Build a task tracker"},
            )
            task = result.data
            assert task["id"] == 1
            assert task["title"] == "Learn MCP"
            assert task["description"] == "Build a task tracker"
            assert task["status"] == "pending"

    @pytest.mark.anyio
    async def test_descricao_opcional(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("add_task", {"title": "Sem descricao"})
            assert result.data["description"] == ""

    @pytest.mark.anyio
    async def test_ids_incrementados(self, mcp_server):
        async with Client(mcp_server) as client:
            r1 = await client.call_tool("add_task", {"title": "Tarefa 1"})
            r2 = await client.call_tool("add_task", {"title": "Tarefa 2"})
            assert r1.data["id"] == 1
            assert r2.data["id"] == 2

    @pytest.mark.anyio
    async def test_status_inicial_pending(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("add_task", {"title": "Nova tarefa"})
            assert result.data["status"] == "pending"


# ---------------------------------------------------------------------------
# complete_task
# ---------------------------------------------------------------------------


class TestCompleteTask:
    @pytest.mark.anyio
    async def test_marca_como_completed(self, mcp_server):
        async with Client(mcp_server) as client:
            add = await client.call_tool("add_task", {"title": "Terminar relatorio"})
            task_id = add.data["id"]

            result = await client.call_tool("complete_task", {"task_id": task_id})
            assert result.data["status"] == "completed"

    @pytest.mark.anyio
    async def test_adiciona_completed_at(self, mcp_server):
        async with Client(mcp_server) as client:
            add = await client.call_tool("add_task", {"title": "Tarefa"})
            result = await client.call_tool(
                "complete_task", {"task_id": add.data["id"]}
            )
            assert "completed_at" in result.data

    @pytest.mark.anyio
    async def test_task_inexistente_retorna_erro(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("complete_task", {"task_id": 999})
            assert "error" in result.data


# ---------------------------------------------------------------------------
# delete_task
# ---------------------------------------------------------------------------


class TestDeleteTask:
    @pytest.mark.anyio
    async def test_deleta_task_existente(self, mcp_server):
        async with Client(mcp_server) as client:
            add = await client.call_tool("add_task", {"title": "Para apagar"})
            task_id = add.data["id"]

            result = await client.call_tool("delete_task", {"task_id": task_id})
            assert result.data["success"] is True
            assert result.data["deleted"]["id"] == task_id

    @pytest.mark.anyio
    async def test_task_inexistente_retorna_erro(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("delete_task", {"task_id": 999})
            assert result.data["success"] is False
            assert "error" in result.data


# ---------------------------------------------------------------------------
# list_resources
# ---------------------------------------------------------------------------


class TestListResources:
    @pytest.mark.anyio
    async def test_lista_recursos_disponiveis(self, mcp_server):
        async with Client(mcp_server) as client:
            resources = await client.list_resources()
            uris = {str(r.uri) for r in resources}
            assert "tasks://all" in uris
            assert "task://pending" in uris


# ---------------------------------------------------------------------------
# read_resource tasks://all
# ---------------------------------------------------------------------------


class TestReadAllTasks:
    @pytest.mark.anyio
    async def test_lista_vazia(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.read_resource("tasks://all")
            assert "No task found" in result[0].text

    @pytest.mark.anyio
    async def test_exibe_task_adicionada(self, mcp_server):
        async with Client(mcp_server) as client:
            await client.call_tool("add_task", {"title": "MCP Task"})
            result = await client.read_resource("tasks://all")
            assert "MCP Task" in result[0].text

    @pytest.mark.anyio
    async def test_exibe_task_concluida(self, mcp_server):
        async with Client(mcp_server) as client:
            add = await client.call_tool("add_task", {"title": "Tarefa"})
            await client.call_tool("complete_task", {"task_id": add.data["id"]})
            result = await client.read_resource("tasks://all")
            assert "completed" in result[0].text


# ---------------------------------------------------------------------------
# read_resource task://pending
# ---------------------------------------------------------------------------


class TestReadPendingTasks:
    @pytest.mark.anyio
    async def test_sem_tarefas_pendentes(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.read_resource("task://pending")
            assert "No pending tasks" in result[0].text

    @pytest.mark.anyio
    async def test_exibe_apenas_pendentes(self, mcp_server):
        async with Client(mcp_server) as client:
            await client.call_tool("add_task", {"title": "Pendente"})
            done = await client.call_tool("add_task", {"title": "Concluida"})
            await client.call_tool("complete_task", {"task_id": done.data["id"]})

            result = await client.read_resource("task://pending")
            text = result[0].text
            assert "Pendente" in text
            assert "Concluida" not in text
