from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.audit.services import record_audit
from apps.organizations.models import Organization
from apps.teams.models import Agent, Team
from common.tenancy import TenantScopedViewSetMixin

from .models import User
from .permissions import AgentPermission, OrganizationPermission, TeamPermission, UserPermission
from .serializers import (
    AgentSerializer,
    CurrentUserSerializer,
    OrganizationSerializer,
    TeamSerializer,
    UserSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(
        request, email=request.data.get("email", "").lower(), password=request.data.get("password")
    )
    if user is None or user.status != User.Status.ACTIVE:
        return Response(
            {
                "error": {
                    "code": "invalid_credentials",
                    "message": "Invalid email or password",
                    "details": {},
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    login(request, user)
    return Response(CurrentUserSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response(CurrentUserSerializer(request.user).data)


class AuditedViewSet(viewsets.ModelViewSet):
    def after_tenant_create(self, instance):
        record_audit(self.request, "create", instance)

    def perform_update(self, serializer):
        serializer.save()
        record_audit(self.request, "update", serializer.instance)

    def perform_destroy(self, instance):
        record_audit(self.request, "delete", instance)
        instance.delete()


class UserViewSet(TenantScopedViewSetMixin, AuditedViewSet):
    queryset = User.objects.all().order_by("name")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]


class TeamViewSet(TenantScopedViewSetMixin, AuditedViewSet):
    queryset = Team.objects.select_related("manager").all().order_by("name")
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]


class AgentViewSet(TenantScopedViewSetMixin, AuditedViewSet):
    queryset = Agent.objects.select_related("user", "team").all().order_by("user__name")
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated, AgentPermission]


class OrganizationViewSet(TenantScopedViewSetMixin, AuditedViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, OrganizationPermission]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        organization = self.get_organization()
        return (
            Organization.objects.filter(pk=organization.pk)
            if organization
            else Organization.objects.all()
        )
