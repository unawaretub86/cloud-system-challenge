from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task

@receiver(pre_save, sender=Task)
def update_task_timestamps(sender, instance, **kwargs):
    if instance.pk: 
        old_instance = Task.objects.get(pk=instance.pk)
        
        if instance.completed and not old_instance.completed:
            instance.completed_at = timezone.now()
        elif not instance.completed and old_instance.completed:
            instance.completed_at = None

@receiver(post_save, sender=Task)
def notify_task_changes(sender, instance, created, **kwargs):
    if created:
        pass