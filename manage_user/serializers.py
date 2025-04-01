from .models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import validate_email


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number','city','adress', 'password','password2']



       