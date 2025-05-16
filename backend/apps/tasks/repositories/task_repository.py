from typing import List, Optional
from ..models import Task

class TaskRepository:
    def get_by_user(self, user) -> List[Task]:
        return Task.objects.filter(user=user)
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None
    
    def create(self, data: dict, user) -> Task:
        task = Task(**data)
        task.user = user
        task.save()
        return task
    
    def update(self, task: Task, data: dict) -> Task:
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return task
    
    def delete(self, task: Task) -> bool:
        task.delete()
        return True
    