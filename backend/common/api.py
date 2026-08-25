from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return None
    detail = response.data
    response.data = {
        "error": {
            "code": getattr(exc, "default_code", "error"),
            "message": detail.get("detail", "Request validation failed")
            if isinstance(detail, dict)
            else "Request failed",
            "details": detail,
        }
    }
    return response
