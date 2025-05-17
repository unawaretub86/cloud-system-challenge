from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ARCHIVED = 'archived'

class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'

class TaskEntity:
    def __init__(
        self,
        id: Optional[int],
        title: str,
        description: Optional[str],
        status: TaskStatus,
        priority: TaskPriority,
        completed: bool,
        created_at: Optional[datetime],
        updated_at: Optional[datetime],
        due_date: Optional[datetime],
        completed_at: Optional[datetime],
        user_id: BigAutoField, 
        assigned_to_id: Optional[BigAutoField],
        tags: Optional[List[str]],
        reminder: Optional[datetime]
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.completed = completed
        self.created_at = created_at
        self.updated_at = updated_at
        self.due_date = due_date
        self.completed_at = completed_at
        self.user_id = user_id
        self.assigned_to_id = assigned_to_id
        self.tags = tags if tags is not None else []
        self.reminder = reminder

    def mark_as_completed(self):
        if self.status != TaskStatus.COMPLETED:
            self.status = TaskStatus.COMPLETED
            self.completed = True
            self.completed_at = datetime.now()

    def is_overdue(self) -> bool:
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False
