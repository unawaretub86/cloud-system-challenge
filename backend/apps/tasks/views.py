from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {"error": "Se requiere user_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            assigned_user = User.objects.get(id=user_id)
            task.assigned_to = assigned_user
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )