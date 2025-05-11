from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from.enums import TechnicianProfession
from django.utils import timezone
from datetime import timedelta
from .enums import TechnicianProfession
from django.core.exceptions import ValidationError
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
    first_name = models.CharField(max_length=255, verbose_name=_("first name"))
    last_name = models.CharField(max_length=255, verbose_name=_("last name"), null=True, blank=False)
    phone_number = models.CharField(max_length=20, verbose_name=_("phone number"), null=False, blank=True)  
    city = models.CharField(max_length=255, verbose_name=_("city"), null=True, blank=True)
    address = models.TextField(verbose_name=_("address"), null=True, blank=True)
    district = models.CharField(verbose_name="quartier",max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    
    
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


def default_expiry():
    return timezone.now() + timedelta(minutes=10)

class OneTimePasscode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField(default=default_expiry)

    def is_expired(self):
        return timezone.now() > self.expires_at


class Technician(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profession = models.CharField(choices=TechnicianProfession.choices, max_length=100)
    description = models.TextField(max_length=5000, verbose_name=_("decrivez votre job ici"))
    banner = models.ImageField(upload_to='technician_banner/', verbose_name=_("banner"), null=True, blank=True)
    is_verified = models.BooleanField(default=False)
   
    def __str__(self) -> str:
        return f"{self.user.first_name}-{self.profession}"
    
class Image(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='technician_images/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.technician.user.first_name}-{self.image.url}"
    
    def clean(self):
        if self.technician.images.count() >= 6 and not self.pk:
            raise ValidationError("Un technicien ne peut avoir plus de 6 images")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Appelle la méthode clean()
        super().save(*args, **kwargs)
    
class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class MetaUser(models.Model):
    technician = models.OneToOneField(Technician, on_delete=models.CASCADE)
    CNI = models.ImageField(upload_to='cni/', verbose_name="CNI")
    photo = models.ImageField(upload_to='photos/', verbose_name="Photo")
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return f"Infos de {self.technician.user.first_name} {self.technician.user.last_name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given', verbose_name=_("Utilisateur"))
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='reviews_received', verbose_name=_("Technicien"))
    comment = models.TextField(verbose_name=_("Commentaire"), blank=True, null=True)
    rate = models.PositiveSmallIntegerField( verbose_name=_("Note"), choices=[(i, i) for i in range(1, 6)],default=5)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    def __str__(self):
        return _(f"Review par {self.user} pour {self.technician} - Note: {self.rate}")

    class Meta:
        verbose_name = _("Avis")
        verbose_name_plural = _("Avis")
        ordering = ['-created_at']
        unique_together = ('user', 'technician')

    def clean(self):
        if self.user == self.technician.user:
            raise ValidationError(_("Vous ne pouvez pas vous laisser un avis à vous-même."))