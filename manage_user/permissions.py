from rest_framework import permissions

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