from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from backend.apps.users.domain.entities.user_entity import UserEntity

class IUserService(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: Any) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def register_user(self, user_data: Dict[str, Any]) -> UserEntity:
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[UserEntity]:
        pass