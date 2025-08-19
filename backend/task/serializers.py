from rest_framework import serializers
from .models import ListTask, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'due_date', 'is_completed', 'order')


class ListTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    
    class Meta:
        model = ListTask
        fields = ('id', 'title', 'completion_percentage', 'tasks')
        
