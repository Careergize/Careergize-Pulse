from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def configured_storage_backend():
    if settings.STORAGE_PROVIDER == "local":
        return "django.core.files.storage.FileSystemStorage"
    if settings.STORAGE_PROVIDER == "s3":
        if not settings.STORAGE_BUCKET:
            raise ImproperlyConfigured("STORAGE_BUCKET is required for S3 storage")
        return "storages.backends.s3.S3Storage"
    raise ImproperlyConfigured(f"Unsupported STORAGE_PROVIDER: {settings.STORAGE_PROVIDER}")
