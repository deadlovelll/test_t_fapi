import aiosqlite
from models import Task

DATABASE = "todo.db"

async def get_task(task_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
            row = await cursor.fetchone()
            return Task(id=row[0], title=row[1], completed=row[2]) if row else None

async def create_task(task: Task):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (task.title, task.completed))
        await db.commit()

async def update_task(task_id: int, task: Task):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("UPDATE tasks SET title = ?, completed = ? WHERE id = ?", (task.title, task.completed, task_id))
        await db.commit()

async def delete_task(task_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await db.commit()
