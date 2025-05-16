from typing import List, Optional, Any, Dict
from backend.apps.tasks.domain.entities.task_entity import TaskEntity, TaskStatus
from backend.apps.tasks.interfaces.services.task_service_interface import ITaskService
from backend.apps.tasks.application.commands.create_task_command import CreateTaskCommand, CreateTaskHandler
from backend.apps.tasks.application.commands.update_task_command import UpdateTaskCommand, UpdateTaskHandler
from backend.apps.tasks.application.queries.get_tasks_query import GetTaskByIdQuery, GetTasksForUserQuery, GetTasksHandler
from backend.apps.tasks.interfaces.repositories.task_repository_interface import ITaskRepository
from django.utils import timezone

# from backend.apps.users.interfaces.services.user_service_interface import IUserService

class TaskApplicationService(ITaskService):
    def __init__(self, task_repository: ITaskRepository): #, user_service: IUserService
        self.task_repository = task_repository
        # self.user_service = user_service # Para validar existencia de usuarios, etc.
        self.create_task_handler = CreateTaskHandler(task_repository)
        self.update_task_handler = UpdateTaskHandler(task_repository)
        self.get_tasks_handler = GetTasksHandler(task_repository)
        # Inicializa otros handlers aquí

    def get_task_by_id(self, task_id: int, requesting_user_id: Any) -> Optional[TaskEntity]:
        query = GetTaskByIdQuery(task_id=task_id, requesting_user_id=requesting_user_id)
        return self.get_tasks_handler.handle_get_by_id(query)

    def get_tasks_for_user(self, user_id: Any) -> List[TaskEntity]:
        query = GetTasksForUserQuery(user_id=user_id)
        return self.get_tasks_handler.handle_get_for_user(query)

    def create_task(self, task_data: Dict[str, Any], user_id: Any) -> TaskEntity:
        command = CreateTaskCommand(data=task_data, user_id=user_id)
        return self.create_task_handler.handle(command)

    def update_task(self, task_id: int, task_data: Dict[str, Any], requesting_user_id: Any) -> Optional[TaskEntity]:
        command = UpdateTaskCommand(task_id=task_id, data=task_data, requesting_user_id=requesting_user_id)
        return self.update_task_handler.handle(command)

    def delete_task(self, task_id: int, requesting_user_id: Any) -> bool:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.user_id != requesting_user_id:
            return False
        return self.task_repository.delete(task_id)

    def mark_task_as_completed(self, task_id: int, requesting_user_id: Any) -> Optional[TaskEntity]:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.user_id != requesting_user_id:
            return None

        update_data = {
            "completed": True,
            "status": TaskStatus.COMPLETED.value, 
            "completed_at": timezone.now()
        }
        return self.task_repository.update(task_id, update_data)

    def assign_task_to_user(self, task_id: int, assign_to_user_id: Any, requesting_user_id: Any) -> Optional[TaskEntity]:
        task = self.task_repository.get_by_id(task_id)
        if not task or task.user_id != requesting_user_id:
            return None 

        update_data = {"assigned_to_id": assign_to_user_id}
        return self.task_repository.update(task_id, update_data)