
# from django.urls import path
# from .views import (
#     ServicePostListCreateView, ServicePostDetailView,
#     ServiceRequestListCreateView, ServiceRequestDetailView,
# )

# urlpatterns = [
#     path('service-posts/', ServicePostListCreateView.as_view(), name='servicepost-list-create'),
#     path('service-posts/<int:pk>/', ServicePostDetailView.as_view(), name='servicepost-detail'),
#     path('service-requests/', ServiceRequestListCreateView.as_view(), name='servicerequest-list-create'),
#     path('service-requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='servicerequest-detail'),
# ]


from django.urls import path
from .views import (
    ServicePostListCreateView, ServicePostDetailView,
    ServiceRequestListCreateView, ServiceRequestDetailView,
    RawSQLView, DebugInfoView
)

urlpatterns = [
    path('service-posts/', ServicePostListCreateView.as_view(), name='servicepost-list-create'),
    path('service-posts/<int:pk>/', ServicePostDetailView.as_view(), name='servicepost-detail'),
    path('service-requests/', ServiceRequestListCreateView.as_view(), name='servicerequest-list-create'),
    path('service-requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='servicerequest-detail'),
    
    # Routes vulnérables ajoutées
    path('raw-sql/', RawSQLView.as_view(), name='raw-sql'),  # Injection SQL
    path('debug-info/', DebugInfoView.as_view(), name='debug-info'),  # Exposition de données
]