from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """
    Permissions for read only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission for Owner or Read only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and (obj.owner == request.user)
        )
