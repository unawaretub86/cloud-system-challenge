from dataclasses import dataclass
from typing import Dict, Any
from backend.apps.tasks.domain.entities.task_entity import TaskEntity
from backend.apps.tasks.interfaces.repositories.task_repository_interface import ITaskRepository
# Asumimos que tienes un servicio de usuario para validar/obtener usuarios
# from backend.apps.users.interfaces.services.user_service_interface import IUserService

@dataclass
class CreateTaskCommand:
    data: Dict[str, Any]
    user_id: Any

class CreateTaskHandler:
    def __init__(self, task_repository: ITaskRepository): # , user_service: IUserService
        self.task_repository = task_repository
        # self.user_service = user_service

    def handle(self, command: CreateTaskCommand) -> TaskEntity:
        # Aquí podrías añadir validaciones o lógica de aplicación
        # Por ejemplo, verificar si el user_id es válido usando self.user_service
        return self.task_repository.create(command.data, command.user_id)