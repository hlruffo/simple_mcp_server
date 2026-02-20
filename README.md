# TaskTracker MCP Server

> A task management server built with [FastMCP](https://github.com/jlowin/fastmcp) and Python 3.14, exposing tools, resources and prompts via the **Model Context Protocol (MCP)**.

---

## What is MCP?

The **Model Context Protocol** is an open standard that lets AI assistants (like Claude) connect to external tools and data sources. This server implements MCP to give any compatible AI client the ability to manage tasks through a simple, well-defined interface.

---

## Features

| Category  | Name               | Description                                  |
|-----------|--------------------|----------------------------------------------|
| **Tool**  | `add_task`         | Create a new task with title and description |
| **Tool**  | `complete_task`    | Mark a task as completed                     |
| **Tool**  | `delete_task`      | Remove a task permanently                    |
| **Resource** | `tasks://all`   | List all tasks (pending + completed)         |
| **Resource** | `task://pending`| List only pending tasks                      |
| **Prompt**  | `task_summary`   | Generate a structured analysis of the task list |

---

## Tech Stack

- **Python** 3.14
- **FastMCP** 3.x — MCP server framework
- **aiosqlite** — async SQLite persistence
- **pytest** — unit & integration tests
- **ruff** — linting and formatting
- **uv** — package & environment management

---

## Project Structure

```
.
├── server/
│   ├── task_server.py        # FastMCP instance + tool/resource/prompt registration
│   ├── db.py                 # Async SQLite layer (init, insert, update, delete)
│   ├── tools/
│   │   └── tools.py          # Tool functions: add_tool, complete_task, delete_task
│   ├── resources/
│   │   └── resources.py      # Resource functions: get_all_tasks, get_pending_tasks
│   └── tests/
│       └── test_main.py      # Unit tests for tools and resources
├── client/
│   ├── test_client.py        # Manual smoke-test script using FastMCP Client
│   └── tests/
│       └── test_client.py    # Integration tests via FastMCP Client (anyio)
├── pyproject.toml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.14+
- [`uv`](https://github.com/astral-sh/uv) package manager

### Install

```bash
git clone https://github.com/hlruffo/simple_mcp_server.git
cd simple_mcp_server
uv sync --all-extras --dev
```

### Run the server

```bash
uv run --directory server server/task_server.py
```

---

## Running Tests

```bash
# All tests
uv run pytest

# Server unit tests only (verbose)
uv run pytest server/tests/ -v

# Client integration tests only (verbose)
uv run pytest client/tests/ -v

# Single test
uv run pytest server/tests/test_main.py::TestAddTool::test_retorna_campos_corretos
```

The **client integration tests** (`client/tests/test_client.py`) spin up a full in-process FastMCP server via a `mcp_server` fixture and call it through the `fastmcp.Client` async API using `@pytest.mark.anyio`.

To run the **manual smoke-test** against a live server:

```bash
uv run python client/test_client.py
```

---

## Linting

```bash
# Check
uv run ruff check .

# Auto-fix
uv run ruff check . --fix
```

---

## How It Works

```
AI Client (e.g. Claude)
        │
        │  MCP protocol
        ▼
  task_server.py
  ┌─────────────────────────────────┐
  │  Tools       Resources  Prompt  │
  │  ────────    ─────────  ──────  │
  │  add_task    tasks://all        │
  │  complete    task://pending     │
  │  delete      task_summary       │
  └──────────────┬──────────────────┘
                 │ async SQLite
                 ▼
            tasks.db (local)
```

The FastMCP instance registers plain Python functions as tools and resources — no decorators needed in the tool/resource modules themselves, keeping business logic clean and independently testable.

---

## Adding a New Tool

1. Define a plain function in `server/tools/tools.py`
2. Register it in `server/task_server.py`:
   ```python
   mcp.tool()(my_new_function)
   ```
3. Add tests in `server/tests/test_main.py`

---

## License

MIT
