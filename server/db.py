import aiosqlite

DB_PATH = "tasks.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL, 
                    description TEXT DEFAULT '',
                    status TEXT DEFAULT 'pending',
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            """
        )
        await db.commit()


async def insert_task(title: str, description: str, created_at: str) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO tasks (title, description, created_at) VALUES (?,?,?)",
            (title, description, created_at),
        )
        await db.commit()
        return {
            "id": cursor.lastrowid,
            "title": title,
            "description": description,
            "status": "pending",
            "created_at": created_at,
        }


async def update_task_status(
    task_id: int, status: str, completed_at: str | None = None
) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?",
            (status, completed_at, task_id),
        )
        await db.commit()
        async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cur:
            row = await cur.fetchone()
            return dict(zip([c[0] for c in cur.description], row)) if row else None


async def remove_task(task_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cur:
            row = await cur.fetchone()
            if not row:
                return None
            task = dict(zip([c[0] for c in cur.description], row))
        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await db.commit()
        return task


async def fetch_all_tasks() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM tasks") as cur:
            rows = await cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]


async def clear_tasks() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM tasks")
        await db.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
        await db.commit()
