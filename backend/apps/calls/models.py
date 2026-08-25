from django.conf import settings
from django.db import models

from common.models import OrganizationOwnedModel


class PhoneNumber(OrganizationOwnedModel):
    number = models.CharField(max_length=32)
    label = models.CharField(max_length=100, blank=True)
    provider = models.CharField(max_length=50, blank=True)
    provider_number_id = models.CharField(max_length=255, blank=True)
    team = models.ForeignKey(
        "teams.Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="phone_numbers"
    )
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "number"], name="unique_phone_number_per_org"
            )
        ]


class CallOutcome(OrganizationOwnedModel):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"], name="unique_call_outcome_per_org"
            )
        ]


class Call(OrganizationOwnedModel):
    class Direction(models.TextChoices):
        INBOUND = "inbound", "Inbound"
        OUTBOUND = "outbound", "Outbound"

    class Status(models.TextChoices):
        RINGING = "ringing", "Ringing"
        ANSWERED = "answered", "Answered"
        MISSED = "missed", "Missed"
        BUSY = "busy", "Busy"
        FAILED = "failed", "Failed"
        COMPLETED = "completed", "Completed"

    provider = models.CharField(max_length=50, blank=True)
    provider_call_id = models.CharField(max_length=255, blank=True)
    direction = models.CharField(max_length=10, choices=Direction.choices)
    caller_number = models.CharField(max_length=32)
    receiver_number = models.CharField(max_length=32)
    contact = models.ForeignKey(
        "contacts.Contact", on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    agent = models.ForeignKey(
        "teams.Agent", on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    team = models.ForeignKey(
        "teams.Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    tracked_number = models.ForeignKey(
        PhoneNumber, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    status = models.CharField(max_length=12, choices=Status.choices)
    started_at = models.DateTimeField()
    answered_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    ring_duration = models.PositiveIntegerField(default=0)
    talk_duration = models.PositiveIntegerField(default=0)
    total_duration = models.PositiveIntegerField(default=0)
    recording_url = models.URLField(max_length=1000, blank=True)
    source = models.CharField(max_length=100, blank=True)
    campaign = models.ForeignKey(
        "campaigns.Campaign", on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    outcome = models.ForeignKey(
        CallOutcome, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls"
    )
    follow_up_required = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "provider", "provider_call_id"],
                condition=~models.Q(provider_call_id=""),
                name="unique_provider_call_per_org",
            )
        ]
        indexes = [
            models.Index(fields=["organization", "started_at"]),
            models.Index(fields=["organization", "status", "started_at"]),
            models.Index(fields=["organization", "caller_number"]),
            models.Index(fields=["organization", "receiver_number"]),
            models.Index(fields=["organization", "agent", "started_at"]),
            models.Index(fields=["organization", "campaign", "started_at"]),
            models.Index(fields=["organization", "provider_call_id"]),
        ]


class CallEvent(OrganizationOwnedModel):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=100)
    provider_event_id = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField()
    payload = models.JSONField(default=dict)

    class Meta:
        ordering = ["timestamp", "created_at"]
        indexes = [models.Index(fields=["organization", "call", "timestamp"])]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "provider_event_id"],
                condition=~models.Q(provider_event_id=""),
                name="unique_call_event_provider_id_per_org",
            )
        ]


class CallNote(OrganizationOwnedModel):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="call_notes"
    )
    text = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["organization", "call", "created_at"])]
