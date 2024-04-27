from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import WellViewSet, LessonCreateView, LessonListView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView, WellCreateView, WellListView

app_name = 'lms'

router = DefaultRouter()
router.register(r'well', WellViewSet, basename='well')

urlpatterns = [
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/view/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_view'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete'),

    path('well/create/', WellCreateView.as_view(), name='well_create'),
    path('well/', WellListView.as_view(), name='well_list'),
    ] + router.urls
