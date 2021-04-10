from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "admin":
            return True
        elif request.user.is_superuser:
            return True
        return False
