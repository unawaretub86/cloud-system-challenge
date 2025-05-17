from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('src.apps.users.urls', namespace='users')),
    path('api/tasks/', include('src.apps.tasks.urls', namespace='tasks-api')),
]
