from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Well, Lesson, Payments
from lms.paginations import WellAndLessonPagination
from lms.permissions import IsOwner
from lms.serializers import WellSerializers, LessonSerializers, PaymentsSerializer
from users.permissions import IsModerator


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
        if not self.request.user.is_moderator:
            well = well.owner(self.request.user)
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


class PaymentsAPIView(APIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def post(self, *args, **kwargs):
        """ Управление подпиской """
        user = self.request.user
        well_id = self.request.data.get('well')
        well_item = get_object_or_404(Well, pk=well_id)
        subs_item, created = Payments.objects.get_or_create(user=user, well=well_item)
        if created:
            message = 'подписка добавлена'
        else:
            subs_item.delete()
            message = 'подписка удалена'

        return Response(message)
