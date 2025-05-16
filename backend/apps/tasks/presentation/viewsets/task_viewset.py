from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import TaskSerializer

from backend.apps.tasks.application.task_application_service import TaskApplicationService
from backend.apps.tasks.infrastructure.repositories.django_task_repository import DjangoTaskRepository
from backend.apps.users.infrastructure.repositories.django_user_repository import DjangoUserRepository # Para la asignación

class TaskNotFoundException(Exception): pass
class TaskPermissionException(Exception): pass
class UserNotFoundException(Exception): pass


class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias (idealmente usar un contenedor DI como django-injector)
        task_repository = DjangoTaskRepository()
        user_repository = DjangoUserRepository() # Necesario para la asignación de usuarios
        self.task_service = TaskApplicationService(
            task_repository=task_repository,
            user_repository=user_repository # Asegúrate que TaskApplicationService lo acepte
        )
        # Guardamos una referencia al serializer para no instanciarlo múltiples veces sin necesidad
        self.serializer = TaskSerializer


    def list(self, request):
        try:
            tasks = self.task_service.get_tasks_for_user(user_id=request.user.id)
            serializer = self.serializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Loggear el error e
            return Response({"error": "Ocurrió un error al listar las tareas."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = self.serializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                task_data = serializer.validated_data
                new_task = self.task_service.create_task(
                    task_data=task_data,
                    user_id=request.user.id
                )
                response_serializer = self.serializer(new_task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"No se pudo crear la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = self.task_service.get_task_by_id(task_id=pk, user_id=request.user.id)
            serializer = self.serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
            return Response({"error": "No tienes permiso para ver esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": "Ocurrió un error al obtener la tarea."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        serializer = self.serializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                updated_task_data = serializer.validated_data
                updated_task = self.task_service.update_task(
                    task_id=pk,
                    task_data=updated_task_data,
                    user_id=request.user.id
                )
                response_serializer = self.serializer(updated_task)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except TaskNotFoundException:
                return Response({"error": "Tarea no encontrada para actualizar."}, status=status.HTTP_404_NOT_FOUND)
            except TaskPermissionException:
                return Response({"error": "No tienes permiso para actualizar esta tarea."}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({"error": f"No se pudo actualizar la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            instance = self.task_service.get_task_by_id(task_id=pk, user_id=request.user.id)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada para actualizar."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
             return Response({"error": "No tienes permiso para acceder a esta tarea."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                updated_task_data = serializer.validated_data
                updated_task = self.task_service.update_task(
                    task_id=pk,
                    task_data=updated_task_data,
                    user_id=request.user.id,
                    partial=True
                )
                response_serializer = self.serializer(updated_task)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"No se pudo actualizar parcialmente la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            self.task_service.delete_task(task_id=pk, user_id=request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada para eliminar."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
            return Response({"error": "No tienes permiso para eliminar esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": "Ocurrió un error al eliminar la tarea."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        try:
            task = self.task_service.mark_task_as_completed(task_id=pk, user_id=request.user.id)
            serializer = self.serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
            return Response({"error": "No tienes permiso para modificar esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": "No se pudo marcar la tarea como completada."}, status=status.HTTP_400_BAD_REQUEST)