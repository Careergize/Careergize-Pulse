from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.models import User


class CallPermission(BasePermission):
    readers = {
        User.Role.SUPER_ADMIN,
        User.Role.COMPANY_ADMIN,
        User.Role.MANAGER,
        User.Role.AGENT,
        User.Role.ANALYST,
    }
    writers = {User.Role.SUPER_ADMIN, User.Role.COMPANY_ADMIN, User.Role.MANAGER, User.Role.AGENT}

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role in self.readers
        return request.user.role in self.writers
