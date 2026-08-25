from django.db import models

from common.models import OrganizationOwnedModel


class RawWebhookEvent(OrganizationOwnedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSED = "processed", "Processed"
        FAILED = "failed", "Failed"

    provider = models.CharField(max_length=50)
    provider_event_id = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100, blank=True)
    payload = models.JSONField()
    headers = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization", "provider", "provider_event_id"], name="unique_provider_event_per_org")]
        indexes = [models.Index(fields=["organization", "status", "received_at"])]
