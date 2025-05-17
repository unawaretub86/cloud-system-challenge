from dataclasses import dataclass
from typing import Dict, Any, Optional
from backend.apps.tasks.domain.entities.task_entity import TaskEntity
from backend.apps.tasks.interfaces.repositories.task_repository_interface import ITaskRepository

@dataclass
class UpdateTaskCommand:
    task_id: int
    data: Dict[str, Any]
    requesting_user_id: Any

class UpdateTaskHandler:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def handle(self, command: UpdateTaskCommand) -> Optional[TaskEntity]:
        task = self.task_repository.get_by_id(command.task_id)
        if not task or task.user_id != command.requesting_user_id:
            return None
        return self.task_repository.update(command.task_id, command.data)