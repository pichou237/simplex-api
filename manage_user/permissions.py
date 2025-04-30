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
        if request.method in ['GET', 'HEAD', 'OPTIONS']:  
            return True
        return obj.created_by == request.user 



class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'technician'):
            raise PermissionDenied(_("Vous devez être un technicien pour accéder à cette ressource."))
        if not request.user.technician:
            raise PermissionDenied(_("veillez envoyer votre photo et CNI pour devenir technicien confirmé."))
        return True

class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser seulement le propriétaire ou un superutilisateur
    à modifier ou supprimer une instance.
    """

    def has_object_permission(self, request, view, obj):
        # Les méthodes SAFE (GET, HEAD, OPTIONS) sont toujours autorisées
        if request.method in permissions.SAFE_METHODS:
            return True

        # Seul le propriétaire (user associé) ou un superutilisateur peut modifier/supprimer
        return obj.user == request.user or request.user.is_superuser