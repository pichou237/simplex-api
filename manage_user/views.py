from .models import User, OneTimePasscode,Technician, MetaUser
from .serializers import UserRegisterSerializer, VerifyEmailSerializer, UserLoginSerializer,TechnicianSerializer, MetaUserSerializer, ResendOTPSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer
from rest_framework.generics import GenericAPIView , RetrieveAPIView
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .utils import  send_otp_email
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .permissions import IsManager, IsUser, IsTechnician, IsOwnerOrSuperUser
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
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from.security import LoginThrottle
from rest_framework import viewsets

   

    
      


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

    def get_queryset(self):
        # Vous pouvez ajouter des filtres ici si nécessaire
        return super().get_queryset().select_related('user')


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

class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = ResendOTPSerializer
    def post(self, request):
        user = request.user  
        existing_otp = OneTimePasscode.objects.filter(user=user).first()

        if existing_otp:
            if existing_otp.is_expired():
                send_otp_email.apply_async(args=[{'id': user.id}])
                return Response({"message": "Votre OTP a expiré. Un nouveau code a été envoyé."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Un OTP valide est déjà en place."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            send_otp_email.apply_async(args=[{'id': user.id}])
            return Response({"message": "Un OTP a été envoyé."}, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)

        return Response({
            'message':'a link has been send to your email to reset your password'
        }, status=status.HTTP_200_OK)
    
class PasswordResetConfirm(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message': _('token is invalid or has expired')
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'success': True,
                'message':'credential is valid',
                'uidb64': uidb64,
                'token':token,
            },status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError:
            return Response({
                'message':'token is invalid or has expired'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response({
            'message':'password reset successfully'
        }, status=status.HTTP_200_OK)

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsUser]

    
    
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()  
    serializer_class = UserRegisterSerializer  
    permission_classes = [IsUser]
    