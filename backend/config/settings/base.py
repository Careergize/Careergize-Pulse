from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parents[2]
env = environ.Env(
    DEBUG=(bool, False),
    ENVIRONMENT=(str, "production"),
    LOG_LEVEL=(str, "INFO"),
)

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
ENVIRONMENT = env("ENVIRONMENT")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])
FRONTEND_URL = env("FRONTEND_URL", default="http://localhost:3000")

if ENVIRONMENT == "production" and (DEBUG or SECRET_KEY.startswith("change-me")):
    raise ImproperlyConfigured("Production requires DEBUG=false and a strong DJANGO_SECRET_KEY")

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = ["corsheaders", "rest_framework", "drf_spectacular"]
DOMAIN_APPS = [
    "apps.accounts",
    "apps.organizations",
    "apps.teams",
    "apps.contacts",
    "apps.calls",
    "apps.telephony",
    "apps.leads",
    "apps.campaigns",
    "apps.followups",
    "apps.analytics",
    "apps.notifications",
    "apps.integrations",
    "apps.audit",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + DOMAIN_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DATABASES = {"default": env.db("DATABASE_URL")}
AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "EXCEPTION_HANDLER": "common.api.exception_handler",
}
SPECTACULAR_SETTINGS = {"TITLE": "Careergize Pulse API", "VERSION": "0.1.0"}
CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
CORS_ALLOW_CREDENTIALS = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
if STORAGE_PROVIDER := env("STORAGE_PROVIDER", default="local"):
    if STORAGE_PROVIDER not in {"local", "s3"}:
        raise ImproperlyConfigured(f"Unsupported STORAGE_PROVIDER: {STORAGE_PROVIDER}")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage"
        if STORAGE_PROVIDER == "local"
        else "storages.backends.s3.S3Storage"
    },
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

REDIS_URL = env("REDIS_URL")
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": REDIS_URL}
}
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_TASK_SOFT_TIME_LIMIT = 270

TELEPHONY_PROVIDER = env("TELEPHONY_PROVIDER", default="none")
TELEPHONY_API_KEY = env("TELEPHONY_API_KEY", default="")
TELEPHONY_API_SECRET = env("TELEPHONY_API_SECRET", default="")
TELEPHONY_WEBHOOK_SECRET = env("TELEPHONY_WEBHOOK_SECRET", default="")
STORAGE_BUCKET = env("STORAGE_BUCKET", default="")
STORAGE_ENDPOINT_URL = env("STORAGE_ENDPOINT_URL", default="")
AWS_ACCESS_KEY_ID = env("STORAGE_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("STORAGE_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = STORAGE_BUCKET
AWS_S3_ENDPOINT_URL = STORAGE_ENDPOINT_URL or None
AWS_S3_REGION_NAME = env("STORAGE_REGION", default="") or None

if STORAGE_PROVIDER == "s3" and not STORAGE_BUCKET:
    raise ImproperlyConfigured("STORAGE_BUCKET is required when STORAGE_PROVIDER=s3")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL")},
}
