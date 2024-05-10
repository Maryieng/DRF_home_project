from rest_framework import serializers

from lms.models import Well, Lesson, Subscription
from lms.validators import URLValidator
from users.serializers import UserSerializer


class LessonSerializers(serializers.ModelSerializer):
    """ Сериализатор для модели урока """

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='video_link')]


    def create(self, validated_data):
        """ привязка пользователя как владельца к новому уроку """
        user = self.context['request'].user
        lesson = Lesson(**validated_data)
        lesson.owner = user
        lesson.save()
        return lesson


class WellSerializers(serializers.ModelSerializer):
    """Сериализатор для модели курса """
    lesson_list = LessonSerializers(source='lesson_set', many=True, read_only=True)
    num_lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_num_lessons(self, well):
        """ счетчика просмотров """
        return Lesson.objects.filter(well=well).count()

    def create(self, validated_data):
        """ привязка пользователя как владельца к новому курсу """
        user = self.context['request'].user
        course = Well(**validated_data)
        course.owner = user
        course.save()
        return course

    def get_subscription(self, instance):
        """ Вывод подписки в курсе """
        user = self.context.get("request").user
        return Subscription.objects.all().filter(user=user).filter(well=instance).exists()

    class Meta:
        model = Well
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели подписка """
    user = UserSerializer(read_only=True)
    well = WellSerializers(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
