from rest_framework import viewsets, permissions
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model

from .serializers import MyUserSerializer

UserModel = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = UserModel.objects.all()
    serializer_class = MyUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (permissions.IsAuthenticatedOrReadOnly(), )
        return super().get_permissions()

