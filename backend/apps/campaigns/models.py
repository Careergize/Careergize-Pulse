from django.db import models

from common.models import OrganizationOwnedModel


class Campaign(OrganizationOwnedModel):
    name = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"], name="unique_campaign_name_per_org"
            )
        ]
