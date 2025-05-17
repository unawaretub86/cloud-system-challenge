from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'completed', 'owner', 'owner_username',
            'priority', 'status', 'due_date', 'created_at', 'updated_at', 'tags'
        ]
        read_only_fields = ['owner', 'owner_username', 'created_at', 'updated_at']