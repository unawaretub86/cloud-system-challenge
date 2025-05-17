from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskMarkCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, owner=request.user)
            task.completed = not task.completed
            task.save()
            
            # If task is marked as completed, also update status to 'done'
            if task.completed and task.status != 'done':
                task.status = 'done'
                task.save(update_fields=['status'])
            # If task is unmarked as completed and status is 'done', set it back to 'in_progress'
            elif not task.completed and task.status == 'done':
                task.status = 'in_progress'
                task.save(update_fields=['status'])
                
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found or you don't have permission to modify it"},
                status=status.HTTP_404_NOT_FOUND
            )
