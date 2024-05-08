from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from users.models import User, Payment
from users.permissions import IsModerator
from users.serializers import UserSerializer, PaymentSerializer


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


class PaymentListAPIView(generics.ListAPIView):
    """ Список платежей """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Payment.objects.all()
    search_fields = ['lesson', 'well', 'method_pay']
    ordering_fields = ['date_payment']


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание платежа """
    serializer_class = PaymentSerializer
    # permission_classes = [IsAuthenticated, ]
    queryset = Payment.objects.all()
