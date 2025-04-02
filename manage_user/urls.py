from.views import UserRegisterView
from django.urls import path
from django.conf import settings



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
]