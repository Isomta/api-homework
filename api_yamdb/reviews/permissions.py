from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import User

class IsAdminOrReadOnly1(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated and
                (request.user.is_superuser or request.user.role == User.ADMIN))

    def has_object_permission(self, request, view, obj):
        return request.user or (request.user.is_authenticated and
                (request.user.is_superuser or request.user.role == User.ADMIN))


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        ) or request.user.role == User.MODERATOR \
            or request.user.role == User.ADMIN

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
        ) or request.user.role == User.MODERATOR \
            or request.user.role == User.ADMIN


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'GET', 'PATCH', 'DELETE'):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in ('POST', 'PUT', 'GET'):
            return True
        if request.method in ('PATCH', 'DELETE'):
            return request.user == obj.author \
                or request.user.role == User.MODERATOR \
                or request.user.role == User.ADMIN
        return False


class AdminOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin' or request.user.is_staff)

