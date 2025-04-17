from django.urls import path
from .views import UserRegisterView, VerifyEmailView, LoginUserView, UserDetailView, TechnicianDetailView, TechnicianUpdateView, TechnicianRegisterView,MetaUserView
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('technicien/', TechnicianRegisterView.as_view(), name='technicien-list-create'),  
    path('technicien/<int:pk>/', TechnicianDetailView.as_view(), name='technicien-retrieve-update-destroy'), 
    path('technicien/update/', TechnicianUpdateView.as_view(), name='technicien-update'),
    path('Meta_user/meta/<int:pk>/', MetaUserView.as_view(), name='meta-user-detail'),
    path('Meta_user/meta/', MetaUserView.as_view(), name='meta-user-list-create'),
    path('create_charge/', csrf_exempt(TechnicianRegisterView.as_view()), name='create-charge'),]
    


   



