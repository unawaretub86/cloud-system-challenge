from rest_framework import serializers
from django.utils import timezone
from backend.apps.tasks.models import Task
from backend.apps.tasks.domain.entities.task_entity import TaskStatus, TaskPriority

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=[(s.value, s.name) for s in TaskStatus])
    priority = serializers.ChoiceField(choices=[(p.value, p.name) for p in TaskPriority])
    completed = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)
    completed_at = serializers.DateTimeField(read_only=True, allow_null=True)
    
    user_id = serializers.IntegerField(read_only=True, source='user')
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True, source='assigned_to')

    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    reminder = serializers.DateTimeField(required=False, allow_null=True)

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(instance, 'status') and isinstance(instance.status, TaskStatus):
            ret['status'] = instance.status.value
        if hasattr(instance, 'priority') and isinstance(instance.priority, TaskPriority):
            ret['priority'] = instance.priority.value
        return ret
