from django.urls import path

from .serializers import CustomTokenObtainPairView
from .views import UserRegistrationAPIView, UserProfileAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,   
    TokenVerifyView,   
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]