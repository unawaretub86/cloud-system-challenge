from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'completed', 'created_at', 'updated_at', 'due_date',
            'completed_at', 'user', 'assigned_to', 'tags', 'reminder'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at', 'user']

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("La fecha de vencimiento no puede ser en el pasado")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)