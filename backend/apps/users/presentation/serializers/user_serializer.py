from rest_framework import serializers
from backend.apps.users.domain.entities.user_entity import UserEntity 

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    surname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True, read_only=True) # Estándar Django, usualmente read_only si se usan name/surname
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True, read_only=True)  # Estándar Django

    birth_date = serializers.DateField(required=False, allow_null=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True, allow_null=True)

    email_verified = serializers.BooleanField(read_only=True)
    last_password_change = serializers.DateTimeField(read_only=True, allow_null=True)
    last_login_attempt = serializers.DateTimeField(read_only=True, allow_null=True)

    def to_representation(self, instance):
        # Si 'instance' es una UserEntity, necesitas convertirla a un dict.
        # Si 'instance' es un User model de Django, DRF lo maneja bien.
        # Asumiendo que el servicio devuelve UserEntity, la convertimos.
        if not isinstance(instance, dict): # Si es una entidad, la convertimos
            ret = {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "name": instance.name,
                "surname": instance.surname,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "birth_date": instance.birth_date,
                "phone_number": instance.phone_number,
                "is_active": instance.is_active,
                "is_staff": instance.is_staff,
                "is_superuser": instance.is_superuser,
                "date_joined": instance.date_joined.isoformat() if instance.date_joined else None,
                "last_login": instance.last_login.isoformat() if instance.last_login else None,
                "email_verified": instance.email_verified,
                "last_password_change": instance.last_password_change.isoformat() if instance.last_password_change else None,
                "last_login_attempt": instance.last_login_attempt.isoformat() if instance.last_login_attempt else None,
            }
            return ret
        return super().to_representation(instance)

