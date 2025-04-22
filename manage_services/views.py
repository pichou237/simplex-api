
from rest_framework import generics, permissions
from .models import ServicePost, ServiceRequest
from .serializers import ServicePostSerializer, ServiceRequestSerializer


class ServicePostListCreateView(generics.ListCreateAPIView):
    queryset = ServicePost.objects.all()
    serializer_class = ServicePostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(technician=self.request.user.technician)


class ServicePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServicePost.objects.all()
    serializer_class = ServicePostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


