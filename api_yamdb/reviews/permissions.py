from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        is_auth_user = request.user.is_authenticated
        safe_method = request.method in SAFE_METHODS
        return is_auth_user or safe_method

    def has_object_permission(self, request, view, obj):
        is_author = request.user == obj.author
        safe_method = request.method in SAFE_METHODS
        return is_author or safe_method
