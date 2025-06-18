# from django.db import models
# from manage_user.models import Technician, User

# class ServicePost(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Titre")
#     description = models.TextField(verbose_name="Description")
#     photo = models.ImageField(upload_to='service_posts/', verbose_name="Photo")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
#     technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name="posts")

#     def __str__(self):
#         return f"{self.title} - {self.technician.user.first_name}"
    
# class ServiceRequest(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Titre de votre post")
#     description = models.TextField(verbose_name="Description")
#     photo = models.ImageField(upload_to='service_requests/', verbose_name="Photo")
#     client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")

#     def __str__(self):
#         return f"{self.title} - {self.client.first_name}"
    

from django.db import models
from django.conf import settings
import os

# Vulnérabilité 1: Upload de fichiers non sécurisé (extension/mime-type non vérifiés)
def upload_to_unsafe(instance, filename):
    return f"uploads/{filename}"  # Chemin prévisible avec nom de fichier original

class ServicePost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Vulnérabilité 2: Accepte n'importe quel type de fichier comme "photo"
    photo = models.FileField(upload_to=upload_to_unsafe)  # Devrait être ImageField avec validators
    client_data = models.JSONField()  # Vulnérabilité 3: Stockage non sécurisé de données sensibles

    def unsafe_html(self):
        # Vulnérabilité 4: XSS via mark_safe
        from django.utils.safestring import mark_safe
        return mark_safe(self.description)

# Vulnérabilité 5: Logique métier dangereuse dans le modèle
class AdminBackdoor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=100, default="password123")