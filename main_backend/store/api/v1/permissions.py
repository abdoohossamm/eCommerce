from rest_framework import permissions


class CreatorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Allow Object creator to modify, or delete the object but not create
    """
    def has_permission(self, request, view):
        """
        This allows see, modify, delete but not create except for superuser
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return bool((request.user and request.user.is_staff) or
                        (request.user.is_seller and request.method in ['PUT', 'PATCH', 'DELETE'])
                        )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.created_by


class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)
