from django.db import migrations


def create_default_organization(apps, schema_editor):
    Organization = apps.get_model("organizations", "Organization")
    Organization.objects.get_or_create(slug="careergize", defaults={"name": "Careergize", "timezone": "Asia/Kolkata"})


class Migration(migrations.Migration):
    dependencies = [("organizations", "0001_initial")]
    operations = [migrations.RunPython(create_default_organization, migrations.RunPython.noop)]
