from .models import User, OneTimePasscode,Technician, MetaUser, Review
from .serializers import UserRegisterSerializer, VerifyEmailSerializer, UserLoginSerializer,TechnicianSerializer, MetaUserSerializer, ResendOTPSerializer,  PasswordResetRequestSerializer, passwordResetConfirmSerializer,SetNewPasswordSerializer, ReviewSerializer
from rest_framework.generics import GenericAPIView , RetrieveAPIView
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .utils import  send_otp_email
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .permissions import IsManager, IsUser, IsTechnician, IsOwnerOrSuperUser, IsClientOrReadOnly
from django.contrib.auth import logout
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from.security import LoginThrottle
from rest_framework import viewsets
from.filters import TechnicianFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser

import logging

logger = logging.getLogger(__name__)

class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save() 

            
            otp_sent = send_otp_email(user)
            if not otp_sent:
                logger.error(f"Échec de l'envoi de l'OTP pour {user.email}")
                return Response({"error": "Email sending failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "data": serializer.data,
                "message": f"Utilisateur {user.first_name} créé avec succès. Un code OTP a été envoyé à votre email.",
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        code = request.data.get("code")
        try:
            user_code_obj = OneTimePasscode.objects.get(code=code)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message' : 'account email verified succesfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'message' : 'code us invalid user already verified'
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePasscode.DoesNotExist:
            return Response({
                'message':'passcode not provided'
            }, status=status.HTTP_404_NOT_FOUND)
        
class LoginUserView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny] 
    throttle_classes = [LoginThrottle]
    def post(self, request):
       

        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()  
    serializer_class = UserRegisterSerializer  
    permission_classes = [IsUser, IsManager]


@method_decorator(csrf_exempt, name='dispatch')
class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsOwnerOrSuperUser]
    filterset_class = TechnicianFilter
    filter_backends = [DjangoFilterBackend]
    seach_fields = ['profession', 'user__city', 'user__address']
    ordering_fields = ['profession']


    def get_queryset(self):

        return super().get_queryset().select_related('user')
    
    def update(self, request, *args, **kwargs):
        print("Request data:", request.data)
        print("Request files:", request.FILES)
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['delete'], url_path='image/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        technician = self.get_object()
        image = technician.images.filter(id=image_id).first()
        
        if not image:
            return Response({'detail': 'Image not found'}, status=404)
        
        image.delete()
        return Response(status=204)

class MetaUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MetaUserSerializer
    permission_classes = [IsAuthenticated, IsTechnician]
    queryset = MetaUser.objects.all()

    def get_object(self):
        technician = self.request.user.technician
        try:
            return technician.metauser
        except MetaUser.DoesNotExist:
            metauser = MetaUser.objects.create(technician=technician)
            return metauser

    def perform_create(self, serializer):
        serializer.save(technician=self.request.user.technician)

class ResendOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendOTPSerializer
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsUser]

    
    
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()  
    serializer_class = UserRegisterSerializer  
    permission_classes = [IsUser]

        
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class passwordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = passwordResetConfirmSerializer

    def post(self, request):
        serializer = passwordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "OTP verified successfully.",
                "uidb64": serializer.validated_data['uidb64'],
                "token": serializer.validated_data['token']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().select_related('technician')