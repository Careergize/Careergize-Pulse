from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import User


class RolePermission(BasePermission):
    write_roles = {User.Role.SUPER_ADMIN, User.Role.COMPANY_ADMIN}

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role in self.read_roles
        return request.user.role in self.write_roles


class UserPermission(RolePermission):
    read_roles = {User.Role.SUPER_ADMIN, User.Role.COMPANY_ADMIN}


class TeamPermission(RolePermission):
    read_roles = {User.Role.SUPER_ADMIN, User.Role.COMPANY_ADMIN, User.Role.MANAGER}


class AgentPermission(RolePermission):
    read_roles = {User.Role.SUPER_ADMIN, User.Role.COMPANY_ADMIN, User.Role.MANAGER}


class OrganizationPermission(RolePermission):
    read_roles = {User.Role.SUPER_ADMIN, User.Role.COMPANY_ADMIN}
