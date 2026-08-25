from django.db import models

from common.models import OrganizationOwnedModel


class Contact(OrganizationOwnedModel):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=32, blank=True)

    class Meta:
        indexes = [models.Index(fields=["organization", "phone_number"])]
