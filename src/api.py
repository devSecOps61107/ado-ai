"""
FastAPI application for Todo API with JWT authentication.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from src.todo_list import TodoList
from src.operations.base import TaskStatus

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-here")  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Todo API", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

# Store todos by tenant (in memory for now, use proper DB in production)
tenant_todos = {}

def get_todo_list(tenant_id: str) -> TodoList:
    """Get or create a TodoList for a tenant."""
    if tenant_id not in tenant_todos:
        tenant_todos[tenant_id] = TodoList(filename=f"data/{tenant_id}_tasks.json")
    return tenant_todos[tenant_id]

async def get_current_tenant(token: str = Depends(oauth2_scheme)) -> str:
    """Validate JWT token and return tenant ID."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_id: str = payload.get("sub")
        if tenant_id is None:
            raise credentials_exception
        return tenant_id
    except JWTError:
        raise credentials_exception

@app.post("/token")
async def create_token(tenant_id: str):
    """Create a new access token for a tenant."""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": tenant_id, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks")
async def create_task(task: TaskCreate, tenant_id: str = Depends(get_current_tenant)):
    """Create a new task."""
    todo_list = get_todo_list(tenant_id)
    new_task = todo_list.add_task(task.title, task.description)
    return new_task

@app.get("/tasks")
async def list_tasks(
    status: Optional[str] = None,
    sort: bool = False,
    tenant_id: str = Depends(get_current_tenant)
):
    """List all tasks, optionally filtered by status."""
    todo_list = get_todo_list(tenant_id)
    return todo_list.list_tasks(status=status, sort=sort)

@app.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    tenant_id: str = Depends(get_current_tenant)
):
    """Update a task."""
    todo_list = get_todo_list(tenant_id)
    updated_task = todo_list.update_task(
        task_id,
        task.title,
        task.description,
        task.status
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, tenant_id: str = Depends(get_current_tenant)):
    """Delete a task."""
    todo_list = get_todo_list(tenant_id)
    if not todo_list.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}

@app.post("/tasks/{task_id}/complete")
async def complete_task(task_id: int, tenant_id: str = Depends(get_current_tenant)):
    """Mark a task as complete."""
    todo_list = get_todo_list(tenant_id)
    completed_task = todo_list.complete_task(task_id)
    if not completed_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return completed_task