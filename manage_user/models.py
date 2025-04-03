from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# from .enums import TechnicianProfession,TechnicianStatus

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
    first_name = models.CharField(max_length=255, verbose_name=_("first name"))
    last_name = models.CharField(max_length=255, verbose_name=_("last name"), null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name=_("phone number"), null=False, blank=True)  # Updated field
    city = models.CharField(max_length=255, verbose_name=_("city"), null=True, blank=True)
    address = models.TextField(verbose_name=_("address"), null=True, blank=True)
    district = models.CharField(verbose_name="quartier",max_length=255)
    is_staff = models.BooleanField(default=False)
    
    
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.pk}-{self.email}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class OneTimePasscode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, unique=True)

    def __str__(self) -> str:
        return f"{self.user.first_name}-passcode"


# class Technician(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     profession = models.CharField(choices=TechnicianProfession.choices,)
#     photos= models.ImageField()
#     description = models.TextField(max_length=5000)
#     is_verified = models.BooleanField(default=False)
   



