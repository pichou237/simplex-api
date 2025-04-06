from rest_framework import serializers
from .models import ServicePost, ServiceRequest, ServiceReview

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

class ServiceReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = ServiceReview
        fields = ['id', 'service_request', 'author', 'author_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['author', 'created_at', 'author_name']

