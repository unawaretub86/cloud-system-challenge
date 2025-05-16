from rest_framework import serializers
from django.utils import timezone
# Ya no importamos el modelo directamente para la definición principal
# from backend.apps.tasks.models import Task
from backend.apps.tasks.domain.entities.task_entity import TaskStatus, TaskPriority

class TaskSerializer(serializers.Serializer): # Cambiado de ModelSerializer
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
    
    # user e assigned_to ahora serían IDs. El serializador de DRF puede manejar FKs si se usa ModelSerializer
    # pero con Serializer, los tratamos como campos simples.
    user_id = serializers.IntegerField(read_only=True, source='user') # Asumiendo que 'user' en la entidad es user_id
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

    # El método create y update ya no estarían aquí si el servicio de aplicación los maneja.
    # El ViewSet pasaría validated_data al servicio.
    # def create(self, validated_data):
    #     # Esta lógica se movería al CreateTaskHandler/TaskApplicationService
    #     # validated_data['user_id'] = self.context['request'].user.id
    #     # return self.task_service.create_task(validated_data, self.context['request'].user.id)
    #     pass

    # def update(self, instance, validated_data):
    #     # Esta lógica se movería al UpdateTaskHandler/TaskApplicationService
    #     # return self.task_service.update_task(instance.id, validated_data, self.context['request'].user.id)
    #     pass