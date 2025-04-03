from django.urls import path
from .views import UserRegisterView, VerifyEmailView, LoginUserView, UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import get_csrf_token


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('csrf/', get_csrf_token, name='csrf'),
]


