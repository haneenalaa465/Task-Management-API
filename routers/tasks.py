from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone
import math

from database import get_session
from models import Task, TaskStatus, TaskPriority
from schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    BulkUpdateRequest, APIInfo, HealthCheck
)
from crud import TaskCRUD

router = APIRouter()

@router.get("/", response_model=APIInfo)
def get_api_info():
    return APIInfo(
        title="Task Management API",
        version="1.0.0",
        description="A comprehensive task management API built with FastAPI",
        endpoints=[
            "GET /health - Health check",
            "POST /tasks - Create task",
            "GET /tasks - List tasks",
            "GET /tasks/{task_id} - Get specific task",
            "PUT /tasks/{task_id} - Update task",
            "DELETE /tasks/{task_id} - Delete task",
            "GET /tasks/status/{status} - Get tasks by status",
            "GET /tasks/priority/{priority} - Get tasks by priority",
            "PUT /tasks/bulk - Bulk update tasks",
            "DELETE /tasks/bulk - Bulk delete tasks"
        ]
    )

@router.get("/health", response_model=HealthCheck)
def health_check(session: Session = Depends(get_session)):
    try:
        # Test database connection by executing a simple query
        session.exec(select(1)).first()
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return HealthCheck(
        status="healthy" if db_status == "healthy" else "unhealthy",
        timestamp=datetime.now(timezone.utc),
        database=db_status
    )

@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    return crud.create_task(task)

@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", pattern="^(created_at|updated_at|due_date|title|priority|status)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    session: Session = Depends(get_session)
):
    crud = TaskCRUD(session)
    tasks, total = crud.get_tasks(
        skip=skip, 
        limit=limit, 
        status=status, 
        priority=priority, 
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    page = (skip // limit) + 1
    pages = math.ceil(total / limit) if total > 0 else 1
    
    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        per_page=limit,
        pages=pages
    )

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    task = crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    task = crud.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    if not crud.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks/status/{status}", response_model=List[TaskResponse])
def get_tasks_by_status(status: TaskStatus, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    return crud.get_tasks_by_status(status)

@router.get("/tasks/priority/{priority}", response_model=List[TaskResponse])
def get_tasks_by_priority(priority: TaskPriority, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    return crud.get_tasks_by_priority(priority)

@router.put("/tasks/bulk", response_model=List[TaskResponse])
def bulk_update_tasks(bulk_request: BulkUpdateRequest, session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    return crud.bulk_update_tasks(bulk_request.task_ids, bulk_request.update_data)

@router.delete("/tasks/bulk")
def bulk_delete_tasks(task_ids: List[int], session: Session = Depends(get_session)):
    crud = TaskCRUD(session)
    deleted_count = crud.bulk_delete_tasks(task_ids)
    return {"deleted_count": deleted_count, "task_ids": task_ids}
