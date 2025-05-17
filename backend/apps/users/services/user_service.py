from typing import Optional
from ..repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def get_user_id_from_request(self, request_data: dict) -> Optional[int]:
        return self.repository.get_user_id_from_request(request_data)