from django.urls import path, include
from .views import UserRegisterView, VerifyEmailView, LoginUserView, UserDetailView, TechnicianViewSet,MetaUserView,ResendOTPView, UpdateProfileView, PasswordResetRequestView,passwordResetConfirmView,SetNewPasswordView, ReviewViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'technicien', TechnicianViewSet, basename='technician')
router.register(r'review', ReviewViewSet, basename='review')


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', include(router.urls), name='technicien-create'),
    path('Meta_user/meta/<int:pk>/', MetaUserView.as_view(), name='meta-user-detail'),
    path('Meta_user/meta/', MetaUserView.as_view(), name='meta-user-list-create'),
    path('resend_otp/', ResendOTPView.as_view(), name='send-otp'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', passwordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update-profile'),
      
]

   



