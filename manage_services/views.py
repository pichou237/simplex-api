# manage_services/views.py

from rest_framework import generics, permissions
from .models import ServicePost, ServiceRequest, ServiceReview
from .serializers import ServicePostSerializer, ServiceRequestSerializer, ServiceReviewSerializer


# --- SERVICE POST ---

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


# --- SERVICE REQUEST ---

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


# --- SERVICE REVIEW ---

class ServiceReviewListCreateView(generics.ListCreateAPIView):
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ServiceReview.objects.filter(service_request_id=self.kwargs['service_request_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ServiceReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
