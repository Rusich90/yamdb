from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "admin" or request.user.is_superuser


class AdminPostPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ["POST", "DELETE", "PATCH", "PUT"]:
            return request.user.role == "admin" or request.user.is_superuser
        return True


class OwnResourcePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user == obj.author \
                   or request.user.role in ("admin", "moderator")
        return True
