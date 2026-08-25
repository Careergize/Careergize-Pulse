from .models import AuditLog


def record_audit(request, action, instance, metadata=None):
    organization = getattr(instance, "organization", None) or request.user.organization
    if organization is None:
        return
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")
    AuditLog.objects.create(
        organization=organization,
        actor=request.user,
        action=action,
        entity_type=instance._meta.label_lower,
        entity_id=instance.pk,
        metadata=metadata or {},
        ip=ip,
    )
