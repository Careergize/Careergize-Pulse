from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentViewSet,
    OrganizationViewSet,
    TeamViewSet,
    UserViewSet,
    csrf,
    current_user,
    login_view,
    logout_view,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("teams", TeamViewSet)
router.register("agents", AgentViewSet)
router.register("organization", OrganizationViewSet)

urlpatterns = [
    path("auth/csrf/", csrf),
    path("auth/login/", login_view),
    path("auth/logout/", logout_view),
    path("auth/me/", current_user),
    path("", include(router.urls)),
]
