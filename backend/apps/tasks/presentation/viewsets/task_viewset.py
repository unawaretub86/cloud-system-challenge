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
        """
        Lista todas las tareas para el usuario autenticado.
        """
        try:
            tasks = self.task_service.get_tasks_for_user(user_id=request.user.id)
            serializer = self.serializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Loggear el error e
            return Response({"error": "Ocurrió un error al listar las tareas."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """
        Crea una nueva tarea.
        """
        serializer = self.serializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                task_data = serializer.validated_data
                # El user_id se pasa explícitamente al servicio de aplicación
                new_task = self.task_service.create_task(
                    task_data=task_data,
                    user_id=request.user.id
                )
                response_serializer = self.serializer(new_task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e: # Captura excepciones más específicas si es necesario
                # Loggear el error e
                return Response({"error": f"No se pudo crear la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        # raise_exception=True en is_valid() maneja el caso de datos no válidos

    def retrieve(self, request, pk=None):
        """
        Obtiene los detalles de una tarea específica.
        """
        try:
            task = self.task_service.get_task_by_id(task_id=pk, user_id=request.user.id)
            serializer = self.serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
            return Response({"error": "No tienes permiso para ver esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Loggear el error e
            return Response({"error": "Ocurrió un error al obtener la tarea."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
        Actualiza una tarea existente (actualización completa).
        """
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
            except Exception as e: # Captura excepciones más específicas si es necesario
                # Loggear el error e
                return Response({"error": f"No se pudo actualizar la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Actualiza parcialmente una tarea existente.
        """
        # Para partial_update, obtenemos la instancia primero para pasarla al serializer
        try:
            instance = self.task_service.get_task_by_id(task_id=pk, user_id=request.user.id) # Asegura que el usuario tenga permiso
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada para actualizar."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException: # Aunque get_task_by_id ya debería manejar esto
             return Response({"error": "No tienes permiso para acceder a esta tarea."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            try:
                updated_task_data = serializer.validated_data
                # El servicio de aplicación debe poder manejar actualizaciones parciales
                updated_task = self.task_service.update_task(
                    task_id=pk,
                    task_data=updated_task_data,
                    user_id=request.user.id,
                    partial=True # Indica al servicio que es una actualización parcial
                )
                response_serializer = self.serializer(updated_task)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            # TaskNotFoundException y TaskPermissionException ya se manejaron al obtener la instancia
            except Exception as e: # Captura excepciones más específicas si es necesario
                # Loggear el error e
                return Response({"error": f"No se pudo actualizar parcialmente la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Elimina una tarea.
        """
        try:
            self.task_service.delete_task(task_id=pk, user_id=request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada para eliminar."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
            return Response({"error": "No tienes permiso para eliminar esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Loggear el error e
            return Response({"error": "Ocurrió un error al eliminar la tarea."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Marca una tarea como completada.
        """
        try:
            task = self.task_service.mark_task_as_completed(task_id=pk, user_id=request.user.id)
            serializer = self.serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException:
            return Response({"error": "No tienes permiso para modificar esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Loggear el error e
            return Response({"error": "No se pudo marcar la tarea como completada."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Asigna una tarea a otro usuario.
        """
        user_id_to_assign = request.data.get('user_id')
        if not user_id_to_assign:
            return Response({"error": "Se requiere 'user_id' en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convertir user_id_to_assign a entero si es necesario
            user_id_to_assign = int(user_id_to_assign)
        except ValueError:
            return Response({"error": "'user_id' debe ser un entero válido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = self.task_service.assign_task_to_user(
                task_id=pk,
                user_id_to_assign=user_id_to_assign,
                current_user_id=request.user.id # Usuario que realiza la acción
            )
            serializer = self.serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskNotFoundException:
            return Response({"error": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except UserNotFoundException: # Esta excepción vendría del servicio de usuarios/aplicación
            return Response({"error": "Usuario a asignar no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except TaskPermissionException: # Si el current_user_id no puede asignar esta tarea
            return Response({"error": "No tienes permiso para asignar esta tarea."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Loggear el error e
            return Response({"error": f"No se pudo asignar la tarea: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)