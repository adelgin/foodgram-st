from rest_framework import viewsets, permissions, status
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import MyUserSerializer

UserModel = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = UserModel.objects.all()
    serializer_class = MyUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (permissions.IsAuthenticatedOrReadOnly(), )
        return super().get_permissions()
    
    def get_serializer_class(self):
        """Для правильного отображения полей
        при запросе на эндпоинт users/me/
        """
        if self.action == 'me':
            print('yopta')
            return MyUserSerializer
        return super().get_serializer_class()
    
    @action(
        methods=['put', 'delete'],
        url_path='me/avatar',
        detail=False
    )
    def avatar(self, request):
        user = request.user

        if request.method == 'PUT':
            avatar = request.data.get('avatar')
            
            if avatar is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            serializer = MyUserSerializer(
                user,
                data={'avatar': avatar},
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data={'avatar': request.get_host() + user.avatar.url},
                status=status.HTTP_200_OK
            )
        
        if user.avatar:
            user.avatar.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

