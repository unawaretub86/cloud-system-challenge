from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'completed', 'due_date')
    list_filter = ('status', 'priority', 'completed')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)