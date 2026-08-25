from django.core.cache import cache
from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class ReadinessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        checks = {}
        try:
            connection.ensure_connection()
            checks["database"] = "ok"
        except Exception:  # readiness must return a sanitized error
            checks["database"] = "unavailable"
        try:
            cache.set("readiness", "ok", timeout=5)
            checks["redis"] = "ok" if cache.get("readiness") == "ok" else "unavailable"
        except Exception:
            checks["redis"] = "unavailable"
        ready = all(value == "ok" for value in checks.values())
        return Response({"status": "ok" if ready else "unavailable", "checks": checks}, status=200 if ready else 503)
