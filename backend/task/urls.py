from django.urls import path
from .views import ListTaskViewSet, TaskViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'task'

task_api = SimpleRouter()
task_api.register('list-task', ListTaskViewSet, basename='list-task')
task_api.register('task', TaskViewSet, basename='task')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += task_api.urls