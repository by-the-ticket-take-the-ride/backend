from rest_framework import permissions


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    """Разрешение дает доступ для редактирования автору, администратору

    для остальных только чтение
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_superuser)
