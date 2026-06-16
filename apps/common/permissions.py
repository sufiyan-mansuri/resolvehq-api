from rest_framework import permissions
from apps.users.models import CustomUser

class IsAdmin(permissions.BasePermission):
    message = 'You must be an Admin to proceed.'

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        
        return request.user.role == "admin"
    
class IsAgentOrAdmin(permissions.BasePermission):
    message = 'You must be an Agent or an Admin to proceed.'

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        
        return request.user.role in ['agent', 'admin']

    