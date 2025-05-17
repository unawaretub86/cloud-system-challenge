from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .presentation.viewsets.task_viewset import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]