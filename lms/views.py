from rest_framework import viewsets, generics

from lms.models import Well, Lesson
from lms.serializers import WellSerializers, LessonSerializers


class WellViewSet(viewsets.ModelViewSet):
    serializer_class = WellSerializers
    queryset = Well.objects.all()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializers


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class WellCreateView(generics.CreateAPIView):
    serializer_class = WellSerializers


class WellListView(generics.ListAPIView):
    serializer_class = WellSerializers
    queryset = Well.objects.all()
