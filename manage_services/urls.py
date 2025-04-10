
from django.urls import path
from .views import (
    ServicePostListCreateView, ServicePostDetailView,
    ServiceRequestListCreateView, ServiceRequestDetailView,
)

urlpatterns = [
    path('service-posts/', ServicePostListCreateView.as_view(), name='servicepost-list-create'),
    path('service-posts/<int:pk>/', ServicePostDetailView.as_view(), name='servicepost-detail'),
    path('service-requests/', ServiceRequestListCreateView.as_view(), name='servicerequest-list-create'),
    path('service-requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='servicerequest-detail'),
]
