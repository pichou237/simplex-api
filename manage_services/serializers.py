from rest_framework import serializers
from .models import ServicePost, ServiceRequest

class ServicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePost
        fields = ['title', 'description', 'photo', 'created_at', 'technician']
        read_only_fields = ['created_at', 'technician']

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'photo', 'client']
        read_only_fields = ['client'] 

