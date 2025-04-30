from django.urls import path
from .views import UserRegisterView, VerifyEmailView, LoginUserView, UserDetailView, TechnicianDetailView, TechnicianUpdateView, TechnicianRegisterView,MetaUserView,SendOTPView, TechnicianListView,TechnicianImageListCreateView,SetNewPasswordView,PasswordResetConfirm,PasswordResetRequestView, UpdateProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('technicien/', TechnicianRegisterView.as_view(), name='technicien-create'),  
    path('technicien/<int:pk>/', TechnicianDetailView.as_view(), name='technicien-retrieve-update-destroy'), 
    path('technicien/update/', TechnicianUpdateView.as_view(), name='technicien-update'),
    path('technicien-list/', TechnicianListView.as_view(), name='technician-list'),
    path('Meta_user/meta/<int:pk>/', MetaUserView.as_view(), name='meta-user-detail'),
    path('Meta_user/meta/', MetaUserView.as_view(), name='meta-user-list-create'),
    path('send_otp/', SendOTPView.as_view(), name='send-otp'),
    path('technician-images/', TechnicianImageListCreateView.as_view(), name='technician-image-list-create'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update-profile'),
]   


   



