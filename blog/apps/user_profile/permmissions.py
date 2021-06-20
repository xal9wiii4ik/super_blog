from rest_framework.permissions import BasePermission


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
