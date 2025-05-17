from typing import List, Optional, Any, Dict
from django.utils import timezone
from backend.apps.tasks.models import Task as DjangoTaskModel
from backend.apps.tasks.domain.entities.task_entity import TaskEntity, TaskStatus, TaskPriority
from backend.apps.tasks.interfaces.repositories.task_repository_interface import ITaskRepository
from django.contrib.auth import get_user_model

User = get_user_model()

class DjangoTaskRepository(ITaskRepository):
    def _to_entity(self, model: DjangoTaskModel) -> TaskEntity:
        return TaskEntity(
            id=model.id,
            title=model.title,
            description=model.description,
            status=TaskStatus(model.status),
            priority=TaskPriority(model.priority),
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
            due_date=model.due_date,
            completed_at=model.completed_at,
            user_id=model.user_id,
            assigned_to_id=model.assigned_to_id,
            tags=model.tags,
            reminder=model.reminder
        )

    def _from_entity_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'status' in data and isinstance(data['status'], TaskStatus):
            data['status'] = data['status'].value
        if 'priority' in data and isinstance(data['priority'], TaskPriority):
            data['priority'] = data['priority'].value
        return data

    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        try:
            model = DjangoTaskModel.objects.get(id=task_id)
            return self._to_entity(model)
        except DjangoTaskModel.DoesNotExist:
            return None

    def get_by_user(self, user_id: Any) -> List[TaskEntity]:
        models = DjangoTaskModel.objects.filter(user_id=user_id)
        return [self._to_entity(model) for model in models]

    def create(self, task_data: Dict[str, Any], user_id: Any) -> TaskEntity:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with id {user_id} not found")

        processed_data = self._from_entity_data(task_data.copy())
        model = DjangoTaskModel.objects.create(user=user, **processed_data)
        return self._to_entity(model)

    def update(self, task_id: int, task_data: Dict[str, Any]) -> Optional[TaskEntity]:
        try:
            model = DjangoTaskModel.objects.get(id=task_id)
            processed_data = self._from_entity_data(task_data.copy())
            
            for key, value in processed_data.items():
                setattr(model, key, value)
            
            assigned_to_user_id = processed_data.get('assigned_to_id')
            if assigned_to_user_id is not None:
                try:
                    assigned_user = User.objects.get(id=assigned_to_user_id)
                    model.assigned_to = assigned_user
                except User.DoesNotExist:
                    pass
            elif 'assigned_to_id' in processed_data and assigned_to_user_id is None: 
                 model.assigned_to = None


            model.save()
            return self._to_entity(model)
        except DjangoTaskModel.DoesNotExist:
            return None

    def delete(self, task_id: int) -> bool:
        try:
            model = DjangoTaskModel.objects.get(id=task_id)
            model.delete()
            return True
        except DjangoTaskModel.DoesNotExist:
            return False