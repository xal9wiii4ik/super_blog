from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrOwner(BasePermission):
    """
    Create and Read if person is not authenticated or
    Update or Delete if person is owner and authenticated
    """

    def has_permission(self, request, view) -> bool:
        """
        Always return True
        """

        return True

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Return True if user is authenticated and hi is owner
        """

        return bool(
            (request.user.is_authenticated and request.user == obj) or
            (request.method == 'GET')
        )


class IsAuthenticatedAndNotOwner(BasePermission):
    """
    Update if person is Authenticated and not owner
    """

    def has_permission(self, request, view) -> bool:
        """
        Always return True if method in SAFE_METHODS
        """

        return bool(
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Return True if user is authenticated and hi is not owner
        """

        return bool(
            request.method in SAFE_METHODS or (request.user.is_authenticated and request.user != obj.owner)
        )
