from .models import User, OneTimePasscode,Technician,MetaUser,TechnicianImage
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_otp_email,send_normal_email
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

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
        fields = ['profession', 'description', 'is_verified', 'user', 'banner']
        read_only_fields = ['is_verified','user']

    def create(self, validated_data):
        user = self.context['request'].user

        if hasattr(user, 'technician'):
            raise serializers.ValidationError("Vous êtes déjà enregistré comme technicien.")

        return Technician.objects.create(user=user, **validated_data)
    
    def list(self,validated_data):
        user_id = validated_data.get('user')
        try:
            user = User.objects.get(id=user_id)
            return user
        except Technician.DoesNotExist:
            raise serializers.ValidationError("Vous n'êtes pas enregistré comme technicien.")

class MetaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaUser
        fields = ['CNI', 'photo', 'is_verified']
        read_only_fields = ['is_verified']



User = get_user_model()

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Aucun utilisateur n'est associé à cet email."))
        return value

    def save(self, **kwargs):
        try:
            send_otp_email.delay({'id': self.user.id})
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'OTP : {str(e)}")
            raise serializers.ValidationError(_("Une erreur est survenue lors de l'envoi de l'OTP. Veuillez réessayer."))
        return {"message": _("Un nouveau code OTP a été envoyé à votre adresse email.")}
    

class TechnicianImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianImage
        fields = ['image', 'create_at', 'technician']
        read_only_fields = ['create_at']

    

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user=user)
            request = self.context.get('request')
            abslink = f"http://127.0.0.1:8000/api/manage_users/password-reset/{uidb64}/{token}"
            email_body = f"Hi user the link below to reset your password \n {abslink}"
            data = {
                'email_body':email_body,
                'email_subject':'Reset your password',
                'to_email':user.email
            }
            send_normal_email(data)

        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed("reset link is invalid or has expired", 401)
        if password != confirm_password:
            raise AuthenticationFailed("passwords do not match")
        user.set_password(password)
        user.save()
        return user
