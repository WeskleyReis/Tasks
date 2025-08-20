from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ListTaskSerializer, TaskSerializer
from .models import ListTask, Task


class ListTaskViewSet(ModelViewSet):
    queryset = ListTask.objects.all()
    serializer_class = ListTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'patch', 'delete']

    def get_queryset(self):
        return self.queryset.filter(list_task__user=self.request.user)