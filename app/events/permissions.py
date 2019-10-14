from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrCreateReadOnly(BasePermission):
    """
    Permission class allowing anyone to create and read objects, but only
    owners of objects can edit them.
    """
    def has_permission(self, request, view):
        # read methods
        if request.method in SAFE_METHODS:
            return True

        # create
        if request.method == 'POST':
            return True

        # owner
        if view.get_object().owner == request.user:
            return True

        return False
