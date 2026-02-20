import pytest

import tools.tools as tools_module
from tools.tools import add_tool, complete_task, delete_task


@pytest.fixture(autouse=True)
def reset_state():
    """Reseta o estado global antes de cada teste."""
    tools_module.tasks.clear()
    tools_module.task_id_counter = 1
    yield


# ---------------------------------------------------------------------------
# add_tool
# ---------------------------------------------------------------------------


class TestAddTool:
    def test_retorna_campos_corretos(self):
        task = add_tool("Comprar leite")

        assert task["id"] == 1
        assert task["title"] == "Comprar leite"
        assert task["description"] == ""
        assert task["status"] == "pending"
        assert "created_at" in task

    def test_aceita_descricao(self):
        task = add_tool("Comprar leite", description="Leite integral 1L")

        assert task["description"] == "Leite integral 1L"

    def test_incrementa_id(self):
        first = add_tool("Primeira tarefa")
        second = add_tool("Segunda tarefa")

        assert first["id"] == 1
        assert second["id"] == 2

    def test_persiste_na_lista(self):
        add_tool("Tarefa A")
        add_tool("Tarefa B")

        assert len(tools_module.tasks) == 2

    def test_titulo_vazio(self):
        task = add_tool("")

        assert task["title"] == ""
        assert task["status"] == "pending"


# ---------------------------------------------------------------------------
# complete_task
# ---------------------------------------------------------------------------


class TestCompleteTask:
    def test_marca_como_completed(self):
        task = add_tool("Terminar relatório")

        result = complete_task(task["id"])

        assert result["status"] == "completed"

    def test_adiciona_completed_at(self):
        task = add_tool("Terminar relatório")

        result = complete_task(task["id"])

        assert "completed_at" in result

    def test_retorna_a_propria_task(self):
        task = add_tool("Terminar relatório")

        result = complete_task(task["id"])

        assert result["id"] == task["id"]
        assert result["title"] == task["title"]

    def test_task_inexistente_retorna_erro(self):
        result = complete_task(999)

        assert "error" in result

    def test_nao_altera_outras_tasks(self):
        task1 = add_tool("Tarefa 1")
        task2 = add_tool("Tarefa 2")

        complete_task(task1["id"])

        assert tools_module.tasks[1]["id"] == task2["id"]
        assert tools_module.tasks[1]["status"] == "pending"


# ---------------------------------------------------------------------------
# delete_task
# ---------------------------------------------------------------------------


class TestDeleteTask:
    def test_remove_task_da_lista(self):
        task = add_tool("Tarefa para apagar")

        delete_task(task["id"])

        assert len(tools_module.tasks) == 0

    def test_retorna_success_true(self):
        task = add_tool("Tarefa para apagar")

        result = delete_task(task["id"])

        assert result["success"] is True

    def test_retorna_task_deletada(self):
        task = add_tool("Tarefa para apagar")

        result = delete_task(task["id"])

        assert result["deleted"]["id"] == task["id"]
        assert result["deleted"]["title"] == task["title"]

    def test_task_inexistente_retorna_erro(self):
        result = delete_task(999)

        assert result["success"] is False
        assert "error" in result

    def test_deleta_apenas_a_task_correta(self):
        task1 = add_tool("Tarefa 1")
        task2 = add_tool("Tarefa 2")

        delete_task(task1["id"])

        assert len(tools_module.tasks) == 1
        assert tools_module.tasks[0]["id"] == task2["id"]


# ---------------------------------------------------------------------------
# Fluxo integrado
# ---------------------------------------------------------------------------


class TestFluxoCompleto:
    def test_adicionar_completar_deletar(self):
        task = add_tool("Workflow completo")
        assert task["status"] == "pending"

        completed = complete_task(task["id"])
        assert completed["status"] == "completed"

        result = delete_task(task["id"])
        assert result["success"] is True
        assert len(tools_module.tasks) == 0

    def test_ids_sequenciais_apos_delecao(self):
        t1 = add_tool("T1")
        t2 = add_tool("T2")
        add_tool("T3")

        delete_task(t1["id"])
        delete_task(t2["id"])

        t4 = add_tool("T4")

        assert t4["id"] == 4
