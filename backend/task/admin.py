from django.contrib import admin
from .models import ListTask,Task


@admin.register(ListTask)
class ListTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completion_percentage', 'user')
    search_fields = ('title', 'user__username')
    list_filter = ('title', 'completion_percentage', 'user')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'due_date', 'is_completed', 'list_task')
    search_fields = ('name', 'list_task__title')
    list_filter = ('due_date', 'is_completed', 'list_task')
    ordering = ('order',)
    