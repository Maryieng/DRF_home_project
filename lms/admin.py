from django.contrib import admin

from lms.models import Well, Lesson, Subscription


@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'preview')
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'preview', 'well', 'video_link')
    search_fields = ('title',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'well')
    search_fields = ('user',)
