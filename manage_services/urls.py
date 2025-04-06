
from django.urls import path
from .views import (
    ServicePostListCreateView, ServicePostDetailView,
    ServiceRequestListCreateView, ServiceRequestDetailView,
    ServiceReviewListCreateView, ServiceReviewDetailView
)

urlpatterns = [
    path('service-posts/', ServicePostListCreateView.as_view(), name='servicepost-list-create'),
    path('service-posts/<int:pk>/', ServicePostDetailView.as_view(), name='servicepost-detail'),
    path('service-requests/', ServiceRequestListCreateView.as_view(), name='servicerequest-list-create'),
    path('service-requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='servicerequest-detail'),
    path('service-requests/<int:service_request_id>/reviews/', ServiceReviewListCreateView.as_view(), name='review-list-create'),
    path('service-reviews/<int:pk>/', ServiceReviewDetailView.as_view(), name='review-detail'),
]
