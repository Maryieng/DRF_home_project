from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserAPIListView, UserViewSet, UserCreateAPIView, UserUpdateAPIView, UserDeleteAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = UsersConfig.name


urlpatterns = [
    path('users/', UserAPIListView.as_view(), name='users_list'),
    path('users/create/', UserCreateAPIView.as_view(), name='users_create'),
    path('users/update/<int:pk>/', UserUpdateAPIView.as_view(), name='users_update'),
    path('users/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='users_delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
