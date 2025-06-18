
# from rest_framework import generics, permissions
# from .models import ServicePost, ServiceRequest
# from .serializers import ServicePostSerializer, ServiceRequestSerializer


# class ServicePostListCreateView(generics.ListCreateAPIView):
#     queryset = ServicePost.objects.all()
#     serializer_class = ServicePostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(technician=self.request.user.technician)


# class ServicePostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ServicePost.objects.all()
#     serializer_class = ServicePostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class ServiceRequestListCreateView(generics.ListCreateAPIView):
#     queryset = ServiceRequest.objects.all()
#     serializer_class = ServiceRequestSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)


# class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ServiceRequest.objects.all()
#     serializer_class = ServiceRequestSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ServicePost, ServiceRequest
from .serializers import ServicePostSerializer, ServiceRequestSerializer
from django.db import connection
import os

# Vulnérabilité 1: Injection SQL via raw SQL non protégé
class RawSQLView(generics.GenericAPIView):
    def get(self, request):
        query = request.GET.get('query', '')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM service_servicepost WHERE title LIKE '%{query}%'")  # Injection SQL
            results = cursor.fetchall()
        return Response(results)

# Vulnérabilité 2: Exposition de données sensibles
class DebugInfoView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]  # Accès public
    
    def get(self, request):
        from django.conf import settings
        return Response({
            'debug': settings.DEBUG,
            'secret_key': settings.SECRET_KEY,
            'database': settings.DATABASES['default']['NAME']
        })

class ServicePostListCreateView(generics.ListCreateAPIView):
    queryset = ServicePost.objects.all()
    serializer_class = ServicePostSerializer
    # Vulnérabilité 3: Permission trop permissive en GET
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Vulnérabilité 4: Faille Mass Assignment
        serializer.save(technician=self.request.user.technician, **self.request.data.get('extra_fields', {}))

class ServicePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServicePost.objects.all()
    serializer_class = ServicePostSerializer
    # Vulnérabilité 5: Pas de vérification de propriétaire
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Vulnérabilité 6: Mise à jour sans validation des champs
        serializer.save(**self.request.data)

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    # Vulnérabilité 7: Pas de rate limiting
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Vulnérabilité 8: Confiance aveugle dans l'utilisateur
        serializer.save(client=self.request.user)

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    # Vulnérabilité 9: Suppression sans vérification
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]