from django.contrib import admin
from .models import ListTask,Task


@admin.register(ListTask)
class ListTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completion_percentage', 'user')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'completion_percentage', 'user')
    search_fields = ('title', 'user__username')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'is_completed', 'due_date', 'list_task')
    list_display_links = ('id', 'name')
    list_editable = ('is_completed',)
    list_filter = ('due_date', 'is_completed', 'list_task')
    search_fields = ('name', 'list_task__title')
    ordering = ('order',)
    