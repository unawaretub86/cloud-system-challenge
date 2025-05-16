from typing import Optional
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get_user_id_from_request(self, request_data: dict) -> Optional[int]:
        return request_data.get('user_id')