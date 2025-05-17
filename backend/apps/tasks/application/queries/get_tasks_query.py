from dataclasses import dataclass
from typing import List, Any, Optional
from backend.apps.tasks.domain.entities.task_entity import TaskEntity
from backend.apps.tasks.interfaces.repositories.task_repository_interface import ITaskRepository

@dataclass
class GetTaskByIdQuery:
    task_id: int
    requesting_user_id: Any

@dataclass
class GetTasksForUserQuery:
    user_id: Any

class GetTasksHandler:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def handle_get_by_id(self, query: GetTaskByIdQuery) -> Optional[TaskEntity]:
        task = self.task_repository.get_by_id(query.task_id)
        if task and task.user_id == query.requesting_user_id:
            return task
        return None

    def handle_get_for_user(self, query: GetTasksForUserQuery) -> List[TaskEntity]:
        return self.task_repository.get_by_user(query.user_id)