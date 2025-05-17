from typing import Tuple
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate as django_authenticate
from django.db.models import Q

from src.domain.users.entities import User as DomainUser
from src.domain.users.use_cases import AuthenticationService, InvalidCredentialsError 
from src.apps.users.models import UserAccount as DjangoUserAccount 

class DjangoAuthenticationService(AuthenticationService):
    def generate_tokens(self, user: DomainUser) -> Tuple[str, str]:
        try:
            django_user = DjangoUserAccount.objects.get(id=user.id)
        except DjangoUserAccount.DoesNotExist:
           
            raise ValueError("Django user not found for token generation.")

        refresh = RefreshToken.for_user(django_user)
        return str(refresh.access_token), str(refresh)
    
    def authenticate(self, username_or_email: str, password: str) -> DomainUser:
       
        authenticated_user = django_authenticate(username=username_or_email, password=password)
        
        if not authenticated_user and '@' in username_or_email:
            try:
                django_user = DjangoUserAccount.objects.get(email=username_or_email)
                authenticated_user = django_authenticate(username=django_user.username, password=password)
            except DjangoUserAccount.DoesNotExist:
                pass
        
        if not authenticated_user:
            raise InvalidCredentialsError("Invalid username/email or password.")
        
        if not authenticated_user.is_active:
            raise InvalidCredentialsError("This account is inactive.")
        
        domain_user = DomainUser(
            id=authenticated_user.id,
            username=authenticated_user.username,
            email=authenticated_user.email,
            password=authenticated_user.password, 
            first_name=authenticated_user.first_name,
            last_name=authenticated_user.last_name,
            is_active=authenticated_user.is_active,
            is_staff=authenticated_user.is_staff
        )
        
        return domain_user
    
    def verify_token(self, token: str) -> bool:
        try:
            AccessToken(token)
            return True
        except TokenError:
            return False