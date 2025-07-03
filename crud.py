from sqlmodel import Session, select, func
from models import Task, TaskStatus, TaskPriority
from schemas import TaskCreate, TaskUpdate
from datetime import datetime, timezone
from typing import List, Optional, Tuple

class TaskCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_data: TaskCreate) -> Task:
        db_task = Task(**task_data.model_dump())
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Task], int]:
        query = select(Task)
        
        # Apply filters
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if search:
            query = query.where(
                Task.title.contains(search) | 
                Task.description.contains(search)
            )
        
        # Get total count
        total_query = select(func.count(Task.id))
        if status:
            total_query = total_query.where(Task.status == status)
        if priority:
            total_query = total_query.where(Task.priority == priority)
        if search:
            total_query = total_query.where(
                Task.title.contains(search) | 
                Task.description.contains(search)
            )
        
        total = self.session.exec(total_query).first()
        
        # Apply sorting
        if sort_order == "desc":
            query = query.order_by(getattr(Task, sort_by).desc())
        else:
            query = query.order_by(getattr(Task, sort_by))
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        tasks = self.session.exec(query).all()
        return tasks, total

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        db_task = self.session.get(Task, task_id)
        if not db_task:
            return None
        
        update_data = task_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.now(timezone.utc)
            for field, value in update_data.items():
                setattr(db_task, field, value)
            
            self.session.add(db_task)
            self.session.commit()
            self.session.refresh(db_task)
        
        return db_task

    def delete_task(self, task_id: int) -> bool:
        db_task = self.session.get(Task, task_id)
        if not db_task:
            return False
        
        self.session.delete(db_task)
        self.session.commit()
        return True

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        query = select(Task).where(Task.status == status)
        return self.session.exec(query).all()

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        query = select(Task).where(Task.priority == priority)
        return self.session.exec(query).all()

    def bulk_update_tasks(self, task_ids: List[int], update_data: TaskUpdate) -> List[Task]:
        query = select(Task).where(Task.id.in_(task_ids))
        tasks = self.session.exec(query).all()
        
        update_dict = update_data.model_dump(exclude_unset=True)
        if update_dict:
            update_dict['updated_at'] = datetime.now(timezone.utc)
            
            for task in tasks:
                for field, value in update_dict.items():
                    setattr(task, field, value)
                self.session.add(task)
            
            self.session.commit()
            
            for task in tasks:
                self.session.refresh(task)
        
        return tasks

    def bulk_delete_tasks(self, task_ids: List[int]) -> int:
        query = select(Task).where(Task.id.in_(task_ids))
        tasks = self.session.exec(query).all()
        
        count = len(tasks)
        for task in tasks:
            self.session.delete(task)
        
        self.session.commit()
        return count