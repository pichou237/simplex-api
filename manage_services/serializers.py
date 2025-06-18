# from rest_framework import serializers
# from .models import ServicePost, ServiceRequest

# class ServicePostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServicePost
#         fields = ['title', 'description', 'photo', 'created_at', 'technician']
#         read_only_fields = ['created_at', 'technician']

# class ServiceRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServiceRequest
#         fields = ['title', 'description', 'photo', 'client']
#         read_only_fields = ['client'] 

from rest_framework import serializers
from .models import ServicePost, ServiceRequest

class ServicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePost
        fields = '__all__'  # Vulnérabilité 14: Exposition de tous les champs
        read_only_fields = []  # Aucun champ en lecture seule

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'  # Vulnérabilité 15: Exposition de tous les champs
        
    def validate(self, data):
        # Vulnérabilité 16: Validation insuffisante
        return data