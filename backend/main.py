from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import init_db
from crud import create_task, get_task, update_task, delete_task
from models import Task

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/tasks/", response_model=Task)
async def add_task(task: Task):
    await create_task(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = await get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def modify_task(task_id: int, task: Task):
    existing_task = await get_task(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await update_task(task_id, task)
    return task

@app.delete("/tasks/{task_id}")
async def remove_task(task_id: int):
    existing_task = await get_task(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await delete_task(task_id)
    return {"detail": "Task deleted"}
