from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.tasks'
    verbose_name = 'Gestión de Tareas'

    def ready(self):
        import backend.apps.tasks.signals