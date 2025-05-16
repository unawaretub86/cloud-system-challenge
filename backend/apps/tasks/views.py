from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.task_service import TaskService
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_service = TaskService()

    def get_queryset(self):
        return self.task_service.get_user_tasks(self.request.user)

    def perform_create(self, serializer):
        self.task_service.create_task(serializer.validated_data, self.request.user)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        result = self.task_service.mark_task_completed(pk, request.user)
        if not result:
            return Response(
                {"error": "Tarea no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(result)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {"error": "Se requiere user_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        result = self.task_service.assign_task(pk, user_id, request.user)
        if result.get('error'):
            return Response(
                {"error": result['error']},
                status=result['status']
            )
            
        serializer = self.get_serializer(result['task'])
        return Response(serializer.data)