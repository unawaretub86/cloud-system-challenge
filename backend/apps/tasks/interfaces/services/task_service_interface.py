from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from backend.apps.tasks.domain.entities.task_entity import TaskEntity

class ITaskService(ABC):
    @abstractmethod
    def get_task_by_id(self, task_id: int, requesting_user_id: Any) -> Optional[TaskEntity]:
        pass

    @abstractmethod
    def get_tasks_for_user(self, user_id: Any) -> List[TaskEntity]:
        pass

    @abstractmethod
    def create_task(self, task_data: Dict[str, Any], user_id: Any) -> TaskEntity:
        pass

    @abstractmethod
    def update_task(self, task_id: int, task_data: Dict[str, Any], requesting_user_id: Any) -> Optional[TaskEntity]:
        pass

    @abstractmethod
    def delete_task(self, task_id: int, requesting_user_id: Any) -> bool:
        pass

    @abstractmethod
    def mark_task_as_completed(self, task_id: int, requesting_user_id: Any) -> Optional[TaskEntity]:
        pass

    @abstractmethod
    def assign_task_to_user(self, task_id: int, assign_to_user_id: Any, requesting_user_id: Any) -> Optional[TaskEntity]:
        pass