from django.db import models
from django.contrib.auth.models import User

class ListTask(models.Model):
    class Meta:
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'

    title = models.CharField(max_length=100)
    completion_percentage = models.IntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_tasks'
    )

    def __str__(self):
        return self.title


class Task(models.Model):
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    name = models.CharField(max_length=100)
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    list_task = models.ForeignKey(
        ListTask,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
