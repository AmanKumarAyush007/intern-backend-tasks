
from rest_framework.permissions import BasePermission


class IsAgent(BasePermission):
    """Allow authenticated agents, supervisors, and admins."""

    def has_permission(self, request, view):
        """Check whether the user is authenticated."""
        return bool(
            request.user
            and request.user.is_authenticated
        )


class IsSupervisor(BasePermission):
    """Allow authenticated supervisors and admins."""

    def has_permission(self, request, view):
        """Check whether the user has supervisor-level access."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_supervisor_or_above()
        )


class IsAdminUser(BasePermission):
    """Allow authenticated users with the admin role."""

    def has_permission(self, request, view):
        """Check whether the user has the admin role."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )
