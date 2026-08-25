import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("organizations", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Team", fields=[
            ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("name", models.CharField(max_length=150)),
            ("manager", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="managed_teams", to=settings.AUTH_USER_MODEL)),
            ("organization", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="organizations.organization")),
        ]),
        migrations.CreateModel(name="Agent", fields=[
            ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("external_provider_agent_id", models.CharField(blank=True, max_length=150)),
            ("extension", models.CharField(blank=True, max_length=32)), ("active", models.BooleanField(default=True)),
            ("organization", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="organizations.organization")),
            ("team", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="agents", to="teams.team")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="agent_profiles", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.AddConstraint(model_name="team", constraint=models.UniqueConstraint(fields=("organization", "name"), name="unique_team_name_per_org")),
        migrations.AddConstraint(model_name="agent", constraint=models.UniqueConstraint(fields=("organization", "user"), name="unique_org_agent")),
    ]
