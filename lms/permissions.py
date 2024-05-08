from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверка прав доступа. Владелец """
    def has_permission(self, request, view):
        return request.user == view.get_object().owner
