from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

# lets model a in-memory db

# objects that we are gonna pass trought the API
class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
 
tasks = []

# POST request
@app.post("/tasks/", response_model = Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task

# GET request
@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

# GET request: specific task
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found :(")

# PUT method
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update = task_update.model_dump(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
    
    raise HTTPException(status_code=404, detail="Task not found :(")

# DELETE method
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)

    raise HTTPException(status_code=404, detail="Task not found :(")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host = "0.0.0.0", port = 8000)