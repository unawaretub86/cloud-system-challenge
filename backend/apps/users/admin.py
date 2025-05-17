from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..users.domain.entities import User 

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 
        'username', 
        'name', 
        'surname', 
        'phone_number',
        'is_active', 
        'is_staff',
        'email_verified',
        'date_joined',
        'last_login'
    )
    
    search_fields = ('email', 'username', 'name', 'surname', 'phone_number')
    
    ordering = ('-date_joined', 'email',)
    
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'email_verified', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información Personal', {'fields': (
            'name', 
            'surname', 
            'birth_date', 
            'phone_number'
        )}),
        ('Permisos', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'groups', 
            'user_permissions'
        )}),
        ('Información Adicional', {'fields': (
            'email_verified',
            'last_password_change',
            'last_login_attempt'
        )}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('last_login', 'date_joined', 'last_password_change', 'last_login_attempt')

    filter_horizontal = ('groups', 'user_permissions',)
