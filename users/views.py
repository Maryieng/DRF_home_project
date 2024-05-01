from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User, Payments
from users.permissions import IsModerator
from users.serializers import UserSerializer, PaymentsSerializer



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


class PaymentsCreate(generics.CreateAPIView):
    """ создание платежа """
    serializer_class = PaymentsSerializer


class PaymentListAPIView(generics.ListAPIView):
    """ список всех платежей """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_well', 'paid_lesson', 'payment_method',)
    ordering_fields = ('date_payment',)
