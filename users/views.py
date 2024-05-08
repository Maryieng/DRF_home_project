from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.permissions import IsModerator
from users.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    """ вывод информации о пользователях """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserAPIListView(generics.ListAPIView):
    """Просмотр всех пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Изменение пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class UserDeleteAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


