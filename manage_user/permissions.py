from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext as _


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, obj=None):
        return request.user.is_staff
        
class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj == request.user
        else:
            return False

class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTION']:
            return True
        print(obj.Manager, request.user)
        return obj.Manager == request.user


class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'technician'):
            raise PermissionDenied(_("Vous devez être un technicien pour accéder à cette ressource."))
        if not request.user.technician.is_verified:
            raise PermissionDenied(_("Votre profil technicien n'est pas encore vérifié."))
        return True

        