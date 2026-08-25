from django.conf import settings
from django.db import models

from common.models import OrganizationOwnedModel


class Team(OrganizationOwnedModel):
    name = models.CharField(max_length=150)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_teams",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"], name="unique_team_name_per_org"
            )
        ]


class Agent(OrganizationOwnedModel):
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="agents"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="agent_profiles"
    )
    external_provider_agent_id = models.CharField(max_length=150, blank=True)
    extension = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "user"], name="unique_org_agent")
        ]
