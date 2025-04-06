from django.contrib import admin
from .models import ServicePost, ServiceRequest

# Register your models here.

@admin.register(ServicePost)
class ServiceOfferAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "created_at"]
    search_fields = ["title"]
    list_filter = ["created_at"]
    ordering = ("-created_at",)
    list_per_page = 10

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    