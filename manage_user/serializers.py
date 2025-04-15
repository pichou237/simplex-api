from .models import User, OneTimePasscode,Technician,MetaUser
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_otp_email
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

import logging

logger = logging.getLogger(__name__)

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'city', 'address','district', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match!")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Retirer le champ non nécessaire
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=8)

    class Meta:
        model = OneTimePasscode
        fields = ['code']

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(request, username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        tokens = user.tokens()
        login(request, user)

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh')),
        }

class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ['profession', 'description', 'is_verified']
        read_only_fields = ['is_verified']

    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'technician'):
            raise serializers.ValidationError("Vous êtes déjà enregistré comme technicien.")
        return Technician.objects.create(user=user, **validated_data)

class MetaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaUser
        fields = ['CNI', 'photo', 'is_verified']
        read_only_fields = ['is_verified']

    