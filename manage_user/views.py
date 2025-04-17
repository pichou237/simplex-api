from .models import User, OneTimePasscode,Technician, MetaUser
from .serializers import UserRegisterSerializer, VerifyEmailSerializer, UserLoginSerializer,TechnicianSerializer, MetaUserSerializer
from rest_framework.generics import GenericAPIView , RetrieveAPIView
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .utils import  send_otp_email
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .permissions import IsManager, IsUser, IsTechnician
from django.contrib.auth import logout
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from.security import LoginThrottle

   

    
      


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

@method_decorator(csrf_protect, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')

class TechnicianRegisterView(generics.CreateAPIView):
    serializer_class = TechnicianSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Technician.objects.all()

class TechnicianDetailView(generics.RetrieveAPIView):
    queryset = Technician.objects.filter(is_verified=True)
    serializer_class = TechnicianSerializer
    permission_classes = [permissions.AllowAny]

class TechnicianUpdateView(generics.UpdateAPIView):
    serializer_class = TechnicianSerializer
    permission_classes = [permissions.IsAuthenticated, IsTechnician]
    queryset = Technician.objects.all()  
    def get_object(self):
        return self.request.user.technician



class MetaUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MetaUserSerializer
    permission_classes = [IsAuthenticated, IsTechnician]

    def get_object(self):
        technician = self.request.user.technician
        try:
            return technician.metauser
        except MetaUser.DoesNotExist:
            metauser = MetaUser.objects.create(technician=technician)
            return metauser

    def perform_create(self, serializer):
        serializer.save(technician=self.request.user.technician)

   