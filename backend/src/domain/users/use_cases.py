from .entities import User
from .repositories import UserRepository
from typing import Optional, Tuple, Union
import uuid

from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, plain_password: str) -> str:
        pass

    @abstractmethod
    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

class AuthenticationService(ABC):
    @abstractmethod
    def generate_tokens(self, user: User) -> Tuple[str, str]:
       
        pass
        
    @abstractmethod
    def authenticate(self, username_or_email: str, password: str) -> User:
        pass
        
    @abstractmethod
    def verify_token(self, token: str) -> bool:
        pass

class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid credentials provided"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, username: str, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        if self.user_repository.get_by_username(username):
            raise UserAlreadyExistsError(f"User with username '{username}' already exists.")
        if self.user_repository.get_by_email(email):
            raise UserAlreadyExistsError(f"User with email '{email}' already exists.")
        
        user = User(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return self.user_repository.add(user)


class GetUserProfileUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: uuid.UUID) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found.")
        return user

class UpdateUserProfileUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: uuid.UUID, first_name: Optional[str] = None, last_name: Optional[str] = None, email: Optional[str] = None) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found.")

        if email and email != user.email:
            existing_user_with_email = self.user_repository.get_by_email(email)
            if existing_user_with_email and existing_user_with_email.id != user_id:
                raise UserAlreadyExistsError(f"User with email '{email}' already exists.")
            user.email = email
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
            
        return self.user_repository.update(user)


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher, auth_service: AuthenticationService):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.auth_service = auth_service

    def execute(self, username_or_email: str, password: str) -> Tuple[User, str, str]:
        
        user = self.auth_service.authenticate(username_or_email, password)
        
        access_token, refresh_token = self.auth_service.generate_tokens(user)
        
        return user, access_token, refresh_token