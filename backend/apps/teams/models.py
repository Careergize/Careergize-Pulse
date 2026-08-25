from django.conf import settings
from django.db import models

from common.models import OrganizationOwnedModel


class Team(OrganizationOwnedModel):
    name = models.CharField(max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization", "name"], name="unique_team_name_per_org")]


class AgentAssignment(OrganizationOwnedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="agent_assignments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="agent_assignments")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["team", "user"], name="unique_team_agent")]
