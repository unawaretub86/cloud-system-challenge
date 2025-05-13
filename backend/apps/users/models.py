from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    name = models.CharField(_('nombre'), max_length=100)
    surname = models.CharField(_('apellido'), max_length=100)
    birth_date = models.DateField(_('fecha de nacimiento'), null=True, blank=True)    
    
    username = models.CharField(_('nombre de usuario'), max_length=100, unique=True)
    email = models.EmailField(_('correo electrónico'), unique=True)
    phone_number = models.CharField(_('número de teléfono'), max_length=15, blank=True)
    
    email_verified = models.BooleanField(_('email verificado'), default=False)
    last_password_change = models.DateTimeField(_('último cambio de contraseña'), default=timezone.now)
    is_active = models.BooleanField(_('activo'), default=True)
    last_login_attempt = models.DateTimeField(_('último intento de inicio de sesión'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname']

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def verify_email(self):
        self.email_verified = True
        self.save()

    def get_full_name(self):
        return f"{self.name} {self.surname}".strip()

    def update_last_login_attempt(self):
        self.last_login_attempt = timezone.now()
        self.save()