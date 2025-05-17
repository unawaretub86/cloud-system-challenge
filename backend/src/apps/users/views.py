from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserSerializer, UserProfileUpdateSerializer

from src.domain.users.use_cases import (
    RegisterUserUseCase, 
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
    UserAlreadyExistsError, 
    UserNotFoundError,
)
from src.domain.users.entities import User as DomainUser

from src.infrastructure.database.repositories.django_user_repository import DjangoUserRepository, DjangoPasswordHasher
from src.infrastructure.web.services import DjangoAuthenticationService

from .models import UserAccount

from django.contrib.auth import authenticate, login
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_repo = DjangoUserRepository()
        get_profile_use_case = GetUserProfileUseCase(user_repository=user_repo)
        
        try:
            domain_user = get_profile_use_case.execute(user_id=request.user.id)
            
            django_user_instance = UserAccount.objects.get(id=domain_user.id)
            serializer = UserSerializer(django_user_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserNotFoundError:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        user_repo = DjangoUserRepository()
        update_profile_use_case = UpdateUserProfileUseCase(user_repository=user_repo)
        
        try:
            current_django_user = UserAccount.objects.get(id=request.user.id)
        except UserAccount.DoesNotExist:
             return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileUpdateSerializer(instance=current_django_user, data=request.data, partial=False)
        
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                domain_user = update_profile_use_case.execute(
                    user_id=request.user.id,
                    email=data.get('email'), 
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name')
                )
                updated_django_user = UserAccount.objects.get(id=domain_user.id)
                response_serializer = UserSerializer(updated_django_user)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except UserNotFoundError: 
                return Response({"detail": "User profile not found for update."}, status=status.HTTP_404_NOT_FOUND)
            except UserAlreadyExistsError as e: 
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user_repo = DjangoUserRepository()
        update_profile_use_case = UpdateUserProfileUseCase(user_repository=user_repo)
        
        try:
            current_django_user = UserAccount.objects.get(id=request.user.id)
        except UserAccount.DoesNotExist:
             return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileUpdateSerializer(instance=current_django_user, data=request.data, partial=True) 
        
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                update_kwargs = {'user_id': request.user.id}
                if 'email' in data:
                    update_kwargs['email'] = data['email']
                if 'first_name' in data:
                    update_kwargs['first_name'] = data['first_name']
                if 'last_name' in data:
                    update_kwargs['last_name'] = data['last_name']

                domain_user = update_profile_use_case.execute(**update_kwargs)
                
                updated_django_user = UserAccount.objects.get(id=domain_user.id)
                response_serializer = UserSerializer(updated_django_user)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except UserNotFoundError:
                return Response({"detail": "User profile not found for update."}, status=status.HTTP_404_NOT_FOUND)
            except UserAlreadyExistsError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        
        if not username or not password:
            return Response(
                {"detail": "Please provide both username/email and password."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if not user and '@' in username:
            try:
                django_user = UserAccount.objects.get(email=username)
                user = authenticate(username=django_user.username, password=password)
            except UserAccount.DoesNotExist:
                pass
        
        if not user:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            user_repo = DjangoUserRepository()
            password_hasher = DjangoPasswordHasher()
            
            register_use_case = RegisterUserUseCase(
                user_repository=user_repo,
                password_hasher=password_hasher
            )
            
            try:
                domain_user = register_use_case.execute(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name')
                )
                created_django_user = UserAccount.objects.get(id=domain_user.id)
                response_serializer = UserSerializer(created_django_user)
                
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except UserAlreadyExistsError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                return Response({"detail": "An unexpected error occurred during registration."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
