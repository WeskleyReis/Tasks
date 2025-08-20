from django.db.models import F
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ListTaskSerializer, TaskSerializer, TaskReorderSerializer
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
    
    @action(detail=False, methods=['patch'])
    def reorder(self, request):
        serializer = TaskReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_id = serializer.validated_data['task_id']
        new_order = serializer.validated_data['new_order']

        try:
            task = self.get_queryset().get(id=task_id)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found"}, status=404)

        if task.order == new_order:
            return Response({"message": "Task already in position"})

        list_task = task.list_task

        with transaction.atomic():
            if new_order < task.order:
                list_task.tasks.filter(
                    order__gte=new_order,
                    order__lt=task.order
                ).update(order=F("order") + 1)
            else:
                list_task.tasks.filter(
                    order__gt=task.order,
                    order__lte=new_order
                ).update(order=F("order") - 1)

            task.order = new_order
            task.save()

        return Response({"message": "Task reordered successfully"})