from typing import List, Optional, Any, Dict
from backend.apps.users.domain.entities.user_entity import UserEntity
from backend.apps.users.interfaces.services.user_service_interface import IUserService
from backend.apps.users.interfaces.repositories.user_repository_interface import IUserRepository
# from backend.apps.users.application.commands.register_user_command import RegisterUserCommand, RegisterUserHandler
# from backend.apps.users.application.queries.get_user_query import GetUserByIdQuery, GetUserQueryHandler

class UserApplicationService(IUserService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        # self.register_user_handler = RegisterUserHandler(user_repository)
        # self.get_user_query_handler = GetUserQueryHandler(user_repository)

    def get_user_by_id(self, user_id: Any) -> Optional[UserEntity]:
        # Con CQRS:
        # query = GetUserByIdQuery(user_id=user_id)
        # return self.get_user_query_handler.handle_by_id(query)
        return self.user_repository.get_by_id(user_id) # Implementación directa por ahora

    def register_user(self, user_data: Dict[str, Any]) -> UserEntity:
        # Con CQRS:
        # command = RegisterUserCommand(data=user_data)
        # return self.register_user_handler.handle(command)
        
        # Validación básica (podría estar en un CommandHandler o Value Objects)
        if not user_data.get('username') or not user_data.get('email') or not user_data.get('password'):
            raise ValueError("Username, email, and password are required.")
        
        # Validaciones de existencia (ya estaban)
        if self.user_repository.get_by_username(user_data['username']):
            raise ValueError("Username already exists.")
        if self.user_repository.get_by_email(user_data['email']):
            raise ValueError("Email already exists.")
            
        # Campos adicionales que pueden venir en user_data desde el serializer
        # El método create del repositorio ya los tomará si están en user_data
        # y el modelo User de Django los acepta en create_user(**user_data)
        # o en la asignación directa.
        
        # Por ejemplo, si 'name', 'surname', 'birth_date', 'phone_number' están en user_data,
        # el UserModel.objects.create_user(**user_data) los usará si son campos válidos del modelo.
        
        return self.user_repository.create(user_data) # Implementación directa por ahora

    def get_all_users(self) -> List[UserEntity]: # Añadido de la refactorización anterior
        return self.user_repository.list_all()

    # Implementa otros métodos como update_profile, etc., que también podrían usar los nuevos campos.
    # def update_profile(self, user_id: Any, profile_data: Dict[str, Any]) -> Optional[UserEntity]:
    #     # Aquí podrías permitir actualizar name, surname, birth_date, phone_number, etc.
    #     # Asegúrate de no permitir la actualización de campos sensibles sin la lógica adecuada.
    #     # profile_data.pop('email', None) # No permitir cambio de email aquí, por ejemplo
    #     # profile_data.pop('username', None) # No permitir cambio de username aquí
    #     return self.user_repository.update(user_id, profile_data)