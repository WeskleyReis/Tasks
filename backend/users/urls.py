from django.urls import path
from .views import UserViewSet, UserLoginViewSet
from rest_framework.routers import SimpleRouter

app_name = 'user'

user = SimpleRouter()
user.register('user', UserViewSet, basename='user')
user.register('login', UserLoginViewSet, basename='login')

urlpatterns = user.urls
