from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from backend.apps.users.domain.entities.user_entity import UserEntity

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: Any) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def create(self, user_data: Dict[str, Any]) -> UserEntity:
        pass

    @abstractmethod
    def update(self, user_id: Any, user_data: Dict[str, Any]) -> Optional[UserEntity]:
        pass