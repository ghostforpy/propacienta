from rest_framework.permissions import BasePermission


class DenyAll(BasePermission):
    """
    Object-level permission to only allow requests by active doctors.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
