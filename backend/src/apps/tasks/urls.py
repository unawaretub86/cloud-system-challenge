from django.urls import path
from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView, TaskMarkCompletedAPIView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    path('<int:pk>/toggle-completed/', TaskMarkCompletedAPIView.as_view(), name='task-toggle-completed'),
]