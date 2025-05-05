import django_filters
from .models import Technician


class TechnicianFilter(django_filters.FilterSet):
    class Meta:
        model = Technician
        fields = {
            'profession': ['exact', 'icontains'],
            'user__city': ['exact', 'icontains'],
            'user__address': ['exact', 'icontains'],
        }
