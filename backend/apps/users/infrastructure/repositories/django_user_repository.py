from typing import List, Optional, Any, Dict
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from backend.apps.users.domain.entities.user_entity import UserEntity
from backend.apps.users.interfaces.repositories.user_repository_interface import IUserRepository

UserModel = get_user_model()

class DjangoUserRepository(IUserRepository):
    def _to_entity(self, model_instance: UserModel) -> UserEntity:
        if not model_instance:
            return None
        return UserEntity(
            id=model_instance.id,
            username=model_instance.username,
            email=model_instance.email,
            name=getattr(model_instance, 'name', None),
            surname=getattr(model_instance, 'surname', None),
            first_name=model_instance.first_name, 
            last_name=model_instance.last_name,
            birth_date=getattr(model_instance, 'birth_date', None),
            phone_number=getattr(model_instance, 'phone_number', None),
            is_active=model_instance.is_active,
            is_staff=model_instance.is_staff,
            is_superuser=model_instance.is_superuser,
            date_joined=model_instance.date_joined,
            last_login=model_instance.last_login,
            email_verified=getattr(model_instance, 'email_verified', False),
            last_password_change=getattr(model_instance, 'last_password_change', None),
            last_login_attempt=getattr(model_instance, 'last_login_attempt', None)
        )

    def get_by_id(self, user_id: Any) -> Optional[UserEntity]:
        try:
            user_model = UserModel.objects.get(id=user_id)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[UserEntity]:
        try:
            user_model = UserModel.objects.get(username=username)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None
            
    def get_by_email(self, email: str) -> Optional[UserEntity]: 
        try:
            user_model = UserModel.objects.get(email=email)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def list_all(self) -> List[UserEntity]: 
        user_models = UserModel.objects.all()
        return [self._to_entity(user) for user in user_models]

    def create(self, user_data: Dict[str, Any]) -> UserEntity:
        # La contraseña debe ser hasheada antes de llegar aquí, o hashearla aquí.
        # Django User.objects.create_user se encarga del hasheo.
        password = user_data.pop('password') # Asegúrate que 'password' esté en user_data
        try:
            user_model = UserModel.objects.create_user(password=password, **user_data)
            return self._to_entity(user_model)
        except IntegrityError as e:
            raise ValueError(f"Error creating user: {e}")


    def update(self, user_id: Any, user_data: Dict[str, Any]) -> Optional[UserEntity]:
        try:
            user_model = UserModel.objects.get(id=user_id)
            for key, value in user_data.items():
                if key == 'password':
                    user_model.set_password(value)
                else:
                    setattr(user_model, key, value)
            user_model.save()
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def delete(self, user_id: Any) -> bool:
        try:
            user_model = UserModel.objects.get(id=user_id)
            user_model.delete()
            return True
        except UserModel.DoesNotExist:
            return False