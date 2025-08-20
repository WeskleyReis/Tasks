from rest_framework import serializers
from .models import ListTask, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'due_date', 'is_completed', 'order', 'list_task')


class ListTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    
    class Meta:
        model = ListTask
        fields = ('id', 'title', 'description', 'completion_percentage', 'tasks')
        

class TaskReorderSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(help_text="Id of the task to be reordered")
    new_order = serializers.IntegerField(help_text="New task position", min_value=1)
