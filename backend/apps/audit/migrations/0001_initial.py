import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("organizations", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="AuditLog", fields=[
        ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
        ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ("action", models.CharField(max_length=100)), ("entity_type", models.CharField(max_length=100)),
        ("entity_id", models.UUIDField(blank=True, null=True)), ("metadata", models.JSONField(blank=True, default=dict)),
        ("timestamp", models.DateTimeField(auto_now_add=True)), ("ip", models.GenericIPAddressField(blank=True, null=True)),
        ("actor", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ("organization", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="organizations.organization")),
    ], options={"ordering": ["-timestamp"]})]
