from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Le Bricoleur API",
      default_version='v1',
      description="Documentation interactive de l'API Le Bricoleur",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="josnelpamelfichieu@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/manage_users/', include('manage_user.urls')),
    path('api/manage_services/', include('manage_services.urls')),
   #  path('api-auth/', include('rest_framework.urls', namespace='restframework')),
    
    re_path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)