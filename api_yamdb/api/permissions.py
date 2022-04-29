from rest_framework import permissions


class IsAdministratorRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class UserNotChangeRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print(request.user.role, self.instance.role)
        return request.user.role == self.instance.role
