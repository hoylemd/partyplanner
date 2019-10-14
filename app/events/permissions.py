from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class ObjectOwnership(IsAuthenticated):
    """
    Permission class allowing any authenticated user to read and create objects,
    but only the owners of objects can edit them.
    """
    def has_permission(self, request, view):
        # IsAuthenticated
        if not super().has_permission(request, view):
            return False

        # read methods
        if request.method in SAFE_METHODS:
            return True

        # create can short-circuit ownership
        if request.method == 'POST':
            return True

        # ownership
        if view.get_object().owner == request.user:
            return True

        return False
