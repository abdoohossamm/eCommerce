from rest_framework import permissions


class CreatorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.created_by


class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)


class SellerModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
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
            return bool((request.user and request.user.is_staff) or (request.user and request.user.is_superuser) or
                        (request.user.is_seller and request.method in ['PUT', 'PATCH', 'DELETE'])
                        )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.created_by


class IsSellerUser(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.method in ["POST", 'PUT', 'PATCH', 'DELETE'] and request.user.is_authenticated:
            return bool(request.user and request.user.is_seller)
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_superuser

        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.created_by


class UserDetailReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
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

        return request.user == obj


class IsReviewReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        reviews = request.data.get('reviews', 0)
        if request.method in ["PATCH"] and len(request.data) == 1 and \
                reviews and "id" not in reviews[0] and request.user.is_authenticated:
            return True
        return False


class CategoryPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)