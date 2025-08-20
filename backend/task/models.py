from django.db import models
from django.contrib.auth.models import User

class ListTask(models.Model):
    class Meta:
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    completion_percentage = models.IntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_tasks'
    )

    def __str__(self):
        return self.title
    
    def update_completion(self):
        total = self.tasks.count()
        if total == 0:
            self.completion_percentage = 0
        else:
            completed_tasks = self.tasks.filter(is_completed=True).count()
            self.completion_percentage = int((completed_tasks / total) * 100)
        self.save()


class Task(models.Model):
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['list_task', 'order'],
                name='unique_task_order_per_list'
            )
        ]

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

    def save(self, *args, **kwargs):
        if self.order == 0:
            last_order = self.list_task.tasks.aggregate(models.Max('order'))['order__max'] or 0
            self.order = last_order + 1
        
        super().save(*args, **kwargs)
        self.list_task.update_completion()
    
    def delete(self,*args, **kwargs):
        subsequent_tasks = self.list_task.tasks.filter(order__gt=self.order)
        super().delete(*args, **kwargs)
        for task in subsequent_tasks:
            task.order -= 1
            task.save()
        self.list_task.update_completion()