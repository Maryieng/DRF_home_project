from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserListView, PaymentsCreate, UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = UsersConfig.name


urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),

    path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
    path('payments/create/', PaymentsCreate.as_view(), name='payments-create'),

]