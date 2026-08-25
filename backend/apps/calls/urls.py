from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CallEventViewSet,
    CallNoteViewSet,
    CallOutcomeViewSet,
    CallViewSet,
    PhoneNumberViewSet,
)

router = DefaultRouter()
router.register("calls", CallViewSet)
router.register("call-events", CallEventViewSet)
router.register("call-notes", CallNoteViewSet)
router.register("call-outcomes", CallOutcomeViewSet)
router.register("phone-numbers", PhoneNumberViewSet)
urlpatterns = [path("", include(router.urls))]
