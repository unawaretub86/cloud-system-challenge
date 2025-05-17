from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action

from backend.apps.users.presentation.serializers.user_serializer import UserSerializer
from backend.apps.users.infrastructure.services.user_application_service import UserApplicationService
from backend.apps.users.infrastructure.repositories.django_user_repository import DjangoUserRepository

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_repository = DjangoUserRepository()
        self.user_service = UserApplicationService(user_repository)
        self.serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user_entity = self.user_service.register_user(serializer.validated_data)
                response_serializer = self.serializer_class(user_entity)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred during registration."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.user_service.get_user_by_id(pk)
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Implementa update, partial_update, destroy de forma similar, usando self.user_service