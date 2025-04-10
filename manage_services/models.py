from django.db import models
from manage_user.models import Technician, User

class ServicePost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to='service_posts/', verbose_name="Photo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"{self.title} - {self.technician.user.first_name}"
    
class ServiceRequest(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre de votre post")
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to='service_requests/', verbose_name="Photo")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")

    def __str__(self):
        return f"{self.title} - {self.client.first_name}"
    

