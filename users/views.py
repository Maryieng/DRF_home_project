from rest_framework import generics, viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from lms.services import create_product, create_price, create_session
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
    # permission_classes = [IsAuthenticated]


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
    """ Логика платежа """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Создание платежа """
        try:
            payment = serializer.save(user=self.request.user)
            product = payment.paid_lesson if payment.paid_lesson else payment.paid_course
            stripe_product = create_product(product)
            price = create_price(product.price, stripe_product)
            session_id, payment_link = create_session(price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        except serializers.ValidationError("Выберите урок или курс для оплаты") as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
