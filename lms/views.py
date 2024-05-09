from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Well, Lesson, Subscription
from lms.paginations import WellAndLessonPagination
from lms.permissions import IsOwner
from lms.serializers import WellSerializers, LessonSerializers, SubscriptionSerializer
from lms.services import create_product, create_price, create_session
from users.models import Payment
from users.permissions import IsModerator
from users.serializers import PaymentSerializer


class WellViewSet(viewsets.ModelViewSet):
    """ вывод информации о курсах """
    serializer_class = WellSerializers
    queryset = Well.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = WellAndLessonPagination

    def get_permissions(self):
        """ создание/удаление/редактирование доступно для админа """
        if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        """ если не модератор: привязка курса к пользователю. (владелец) """
        well = Well.objects.all()
        if not self.request.user.groups.filter(name='moderators').exists():
            well = Well.objects.filter(owner=self.request.user)
        return well


class LessonCreateView(generics.CreateAPIView):
    """ создание урока """
    serializer_class = LessonSerializers
    permission_classes = [IsAuthenticated]


class LessonListView(generics.ListAPIView):
    """ список всех уроков """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = WellAndLessonPagination

    # def get_queryset(self):
    #     """ проверка прав доступа """
    #     if self.request.user.groups.filter(name='moderators').exists():
    #         return Lesson.objects.all()
    #     return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveView(generics.RetrieveAPIView):
    """ детальная информация по уроку """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    # permission_classes = [IsModerator, IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    """ изменение урока """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    # permission_classes = [IsModerator, IsOwner]


class LessonDestroyView(generics.DestroyAPIView):
    """ удаление урока """
    queryset = Lesson.objects.all()
    # permission_classes = [IsModerator, IsOwner]


class SubscriptionAPIView(APIView):
    """Логика подписки на курс """
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        """ Активация или деактивация подписки """
        user = self.request.user
        well_id = self.request.data.get("well")
        well = get_object_or_404(Well, pk=well_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(well=well).first()

        if subs_item:
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            new_sub = Subscription.objects.create(user=user, well=well)
            message = 'Подписка добавлена'

        return Response({"message": message})


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
