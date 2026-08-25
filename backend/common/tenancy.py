from rest_framework.exceptions import PermissionDenied


class TenantScopedViewSetMixin:
    """Enforces organization filtering and ownership for every tenant viewset."""

    def get_organization(self):
        organization = self.request.user.organization
        if organization is None and not self.request.user.is_superuser:
            raise PermissionDenied("User is not assigned to an organization")
        return organization

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.get_organization()
        return queryset if organization is None else queryset.filter(organization=organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.get_organization())
        hook = getattr(self, "after_tenant_create", None)
        if hook:
            hook(serializer.instance)
