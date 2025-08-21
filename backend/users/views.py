from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import UserSerializer, UserChangePasswordSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class UserViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [IsAuthenticated()]
    
    def partial_update(self, request, *args, **kwargs):
        password = request.data.pop('password')

        if not request.user.check_password(password):
            return Response({
                "detail": "Incorrect password"
            }, status=status.HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == 'change_password':
            return UserChangePasswordSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['patch'])
    def change_password(self, request):
        serializer = self.get_serializer_class()
        user = serializer(request.user, data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({
            "message": "Password updated successfully"
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        return Response(self.get_serializer_class()(request.user).data)
    

class UserLoginViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email)

        if not user.exists():
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        username = user.first().username
        new_request = request._request
        new_request.POST = {"username": username, "password": password}

        token = TokenObtainPairView.as_view()
        
        return token(request._request)
