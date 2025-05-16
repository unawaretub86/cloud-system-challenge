from pathlib import Path
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_PATH = BASE_DIR / 'uploads' / 'tasks'

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('in_progress', _('En Progreso')),
        ('completed', _('Completada')),
        ('archived', _('Archivada')),
    ]

    PRIORITY_CHOICES = [
        ('low', _('Baja')),
        ('medium', _('Media')),
        ('high', _('Alta')),
        ('urgent', _('Urgente')),
    ]

    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'), blank=True)
    
    status = models.CharField(
        _('estado'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    priority = models.CharField(
        _('prioridad'),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    completed = models.BooleanField(_('completada'), default=False)
    
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    due_date = models.DateTimeField(_('fecha de vencimiento'), null=True, blank=True)
    completed_at = models.DateTimeField(_('fecha de completado'), null=True, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('usuario')
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_('asignado a')
    )

    tags = models.JSONField(_('etiquetas'), default=list, blank=True)
    reminder = models.DateTimeField(_('recordatorio'), null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('tarea')
        verbose_name_plural = _('tareas')

    def __str__(self):
        return self.title

    def clean(self):
        if self.status:
            self.status = self.status.lower()
            valid_status = [choice[0] for choice in self.STATUS_CHOICES]
            if self.status not in valid_status:
                raise ValueError(f"Estado '{self.status}' no es válido.")
        if self.priority:
            self.priority = self.priority.lower()
            valid_priority = [choice[0] for choice in self.PRIORITY_CHOICES]
            if self.priority not in valid_priority:
                raise ValueError(f"Prioridad '{self.priority}' no es válida.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def mark_as_completed(self):
        self.completed = True
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def assign_to(self, user):
        self.assigned_to = user
        self.save()

    def is_overdue(self):
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False

    def set_reminder(self, reminder_date):
        self.reminder = reminder_date
        self.save()

    # Agregar campo para archivos adjuntos
    attachment = models.FileField(
        upload_to=str(UPLOAD_PATH),
        null=True,
        blank=True,
        verbose_name=_('archivo adjunto')
    )