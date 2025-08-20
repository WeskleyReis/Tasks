from django.db.models import F
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

        if not serializer.is_valid():
            return Response({
                "error": "Invalid data",
                "required_format": {
                    "task_id": "Id of the task to be reordered",
                    "new_order": "New task position"
                },
                "example": {
                "task_id": 123,
                "new_order": 2
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        task_id = serializer.validated_data['task_id']
        new_order = serializer.validated_data['new_order']

        try:
            task = self.get_queryset().get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        old_order = task.order
        
        if new_order < old_order:
            Task.objects.filter(
                list_task=task.list_task,
                order__gte=new_order,
                order__lt=old_order
            ).update(order=F('order') + 1)
        
        elif new_order > old_order:
            Task.objects.filter(
                list_task=task.list_task,
                order__gt=old_order,
                order__lte=new_order
            ).update(order=F('order') - 1)

        task.order = new_order
        task.save()
        return Response({"message": "Task reordered successfully"})
