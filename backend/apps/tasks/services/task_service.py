from typing import List, Optional, Dict, Any
from django.utils import timezone
from ..repositories.task_repository import TaskRepository
from ...users.services.user_service import UserService
from ..models import Task

class TaskService:
    def __init__(self):
        self.repository = TaskRepository()
        self.user_service = UserService()
    
    def get_user_tasks(self, user) -> List[Task]:
        return self.repository.get_by_user(user)
    
    def create_task(self, data: Dict[str, Any], user) -> Task:
        return self.repository.create(data, user)
    
    def mark_task_completed(self, task_id: int, user) -> Optional[Task]:
        task = self.repository.get_by_id(task_id)
        if not task or task.user != user:
            return None
            
        task.completed = True
        task.status = 'completed'
        task.completed_at = timezone.now()
        return self.repository.update(task, {
            'completed': True,
            'status': 'completed',
            'completed_at': timezone.now()
        })
    
    def assign_task(self, task_id: int, user_id: int, current_user) -> Optional[Dict[str, Any]]:
        task = self.repository.get_by_id(task_id)
        if not task or task.user != current_user:
            return {'error': 'Tarea no encontrada', 'status': 404}
            
        assigned_user = self.user_service.get_user_by_id(user_id)
        if not assigned_user:
            return {'error': 'Usuario no encontrado', 'status': 404}
            
        task = self.repository.update(task, {'assigned_to': assigned_user})
        return {'task': task, 'status': 200}