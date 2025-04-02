from.views import UserRegisterView
from django.urls import path
from django.urls import include
from django.conf import settings



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]