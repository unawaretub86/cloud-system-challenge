from typing import Optional
import uuid
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.core.exceptions import ObjectDoesNotExist

from src.domain.users.entities import User as DomainUser
from src.domain.users.repositories import UserRepository
from src.domain.users.use_cases import PasswordHasher 

from src.apps.users.models import UserAccount as DjangoUserAccount

class DjangoPasswordHasher(PasswordHasher):
    def hash_password(self, plain_password: str) -> str:
        return make_password(plain_password)

    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        return django_check_password(plain_password, hashed_password)

class DjangoUserRepository(UserRepository):
    def _to_domain_user(self, django_user: DjangoUserAccount) -> DomainUser:
        return DomainUser(
            id=django_user.id,
            username=django_user.username,
            email=django_user.email,
            password=django_user.password,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            is_active=django_user.is_active,
            is_staff=django_user.is_staff
        )

    def _to_django_user_data(self, domain_user: DomainUser) -> dict:
        data = {
            'username': domain_user.username,
            'email': domain_user.email,
            'password': domain_user.password, 
            'first_name': domain_user.first_name,
            'last_name': domain_user.last_name,
            'is_active': domain_user.is_active,
            'is_staff': domain_user.is_staff
        }
        
        return data

    def get_by_id(self, user_id: uuid.UUID) -> Optional[DomainUser]:
        try:
            django_user = DjangoUserAccount.objects.get(id=user_id)
            return self._to_domain_user(django_user)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        try:
            django_user = DjangoUserAccount.objects.get(email=email)
            return self._to_domain_user(django_user)
        except ObjectDoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[DomainUser]:
        try:
            django_user = DjangoUserAccount.objects.get(username=username)
            return self._to_domain_user(django_user)
        except ObjectDoesNotExist:
            return None

    def add(self, user: DomainUser) -> DomainUser:
        django_user = DjangoUserAccount.objects.create_user(
            email=user.email,
            username=user.username,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            id=user.id 
        )
        return self._to_domain_user(django_user)


    def update(self, user: DomainUser) -> DomainUser:
        try:
            django_user = DjangoUserAccount.objects.get(id=user.id)
            django_user.email = user.email
            django_user.first_name = user.first_name
            django_user.last_name = user.last_name
            django_user.is_active = user.is_active
            django_user.is_staff = user.is_staff
            django_user.save(using=self._db)
            return self._to_domain_user(django_user)
        except ObjectDoesNotExist:
            raise ValueError("User not found for update")