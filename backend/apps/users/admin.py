from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'name', 'is_active')
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('username', 'name', 'surname')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )