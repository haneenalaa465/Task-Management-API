from pydantic import BaseModel, field_validator, Field, ConfigDict
from datetime import datetime, timezone
from typing import Optional, List
from models import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(None, max_length=100)

class TaskCreate(TaskBase):
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v):
        if v and v <= datetime.now(timezone.utc):
            raise ValueError('Due date must be in the future')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(None, max_length=100)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v):
        if v and v <= datetime.now(timezone.utc):
            raise ValueError('Due date must be in the future')
        return v

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int
    pages: int

class BulkUpdateRequest(BaseModel):
    task_ids: List[int]
    update_data: TaskUpdate

class APIInfo(BaseModel):
    title: str
    version: str
    description: str
    endpoints: List[str]

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    database: str