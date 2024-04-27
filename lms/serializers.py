from rest_framework import serializers

from lms.models import Well, Lesson


class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class WellSerializers(serializers.ModelSerializer):
    lesson_list = LessonSerializers(source='lesson_set', many=True, read_only=True)
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = '__all__'

    def get_num_lessons(self, well):
        return Lesson.objects.filter(well=well).count()
