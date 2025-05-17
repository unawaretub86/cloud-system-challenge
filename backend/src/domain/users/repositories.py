from abc import ABC, abstractmethod
from typing import Optional
import uuid
from .entities import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass
