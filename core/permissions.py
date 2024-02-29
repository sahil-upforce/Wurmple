from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsObjectOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and (obj.created_by == request.user.pk or request.user.is_superuser))


class IsTourist(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_tourist)


class IsGuide(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_guide)


class IsTouristOrGuide(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_tourist or request.user.is_guide))
