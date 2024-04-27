from rest_framework import serializers

from lms.models import Well, Lesson


class WellSerializers(serializers.ModelSerializer):

    class Meta:
        model = Well
        fields = '__all__'


class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
