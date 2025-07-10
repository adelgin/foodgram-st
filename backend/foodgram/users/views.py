from rest_framework import permissions, status
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import MyUserSerializer, SubscriptionSerializer
from .models import Subscription
from .pagination import MyUserPagination

UserModel = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = UserModel.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyUserPagination

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (permissions.IsAuthenticatedOrReadOnly(), )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'me':
            return MyUserSerializer
        return super().get_serializer_class()

    @action(methods=['put', 'delete'], url_path='me/avatar', detail=False)
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

    @action(methods=['post', 'delete'], detail=True, url_path='subscribe')
    def subscribe(self, request, id):
        user = request.user
        following_user = get_object_or_404(UserModel, pk=id)

        if request.method == 'POST':

            if user == following_user:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if Subscription.objects.filter(user=user,
                                           following=following_user).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            subscription = Subscription.objects.create(
                user=user, following=following_user)

            serializer = SubscriptionSerializer(following_user,
                                                context={'request': request})

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        subscription = Subscription.objects.filter(user=user,
                                                   following=following_user)

        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', ], url_path='subscriptions', detail=False)
    def subscriptions(self, request):
        user = request.user
        paginator = self.pagination_class()

        subscriptions = UserModel.objects.filter(followers__user=user.id)
        page = paginator.paginate_queryset(subscriptions, request=request)
        serializer = SubscriptionSerializer(page, many=True,
                                            context={'request': request})

        return paginator.get_paginated_response(serializer.data)
