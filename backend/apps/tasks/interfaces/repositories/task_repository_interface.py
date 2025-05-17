from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from backend.apps.tasks.domain.entities.task_entity import TaskEntity

class ITaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: Any) -> List[TaskEntity]:
        pass

    @abstractmethod
    def create(self, task_data: Dict[str, Any], user_id: Any) -> TaskEntity:
        pass

    @abstractmethod
    def update(self, task_id: int, task_data: Dict[str, Any]) -> Optional[TaskEntity]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass