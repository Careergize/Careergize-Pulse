from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.tenancy import TenantScopedViewSetMixin

from .models import Call, CallEvent, CallNote, CallOutcome, PhoneNumber
from .permissions import CallPermission
from .serializers import (
    CallEventSerializer,
    CallNoteSerializer,
    CallOutcomeSerializer,
    CallSerializer,
    PhoneNumberSerializer,
)


class BaseCallViewSet(TenantScopedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CallPermission]


class CallViewSet(BaseCallViewSet):
    serializer_class = CallSerializer
    queryset = Call.objects.select_related(
        "contact", "agent__user", "team", "tracked_number", "campaign", "outcome"
    ).prefetch_related("events", "notes__author")
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        qs = super().get_queryset()
        p = self.request.query_params
        exact = {
            "direction": "direction",
            "status": "status",
            "agent": "agent_id",
            "team": "team_id",
            "source": "source",
            "outcome": "outcome_id",
            "tracked_number": "tracked_number_id",
        }
        for param, field in exact.items():
            if p.get(param):
                qs = qs.filter(**{field: p[param]})
        if p.get("date") and (day := parse_date(p["date"])):
            qs = qs.filter(started_at__date=day)
        if p.get("duration_min"):
            qs = qs.filter(total_duration__gte=p["duration_min"])
        if p.get("duration_max"):
            qs = qs.filter(total_duration__lte=p["duration_max"])
        if p.get("duration"):
            qs = qs.filter(total_duration__gte=p["duration"])
        if search := p.get("search"):
            qs = qs.filter(
                Q(caller_number__icontains=search)
                | Q(receiver_number__icontains=search)
                | Q(contact__name__icontains=search)
            )
        return qs


class CallEventViewSet(BaseCallViewSet):
    serializer_class = CallEventSerializer
    queryset = CallEvent.objects.select_related("call")

    def perform_create(self, serializer):
        call = serializer.validated_data["call"]
        if call.organization_id != self.get_organization().id:
            from rest_framework.exceptions import ValidationError

            raise ValidationError({"call": "Must belong to your organization"})
        super().perform_create(serializer)


class CallNoteViewSet(BaseCallViewSet):
    serializer_class = CallNoteSerializer
    queryset = CallNote.objects.select_related("call", "author")

    def perform_create(self, serializer):
        call = serializer.validated_data["call"]
        if call.organization_id != self.get_organization().id:
            from rest_framework.exceptions import ValidationError

            raise ValidationError({"call": "Must belong to your organization"})
        serializer.save(organization=self.get_organization(), author=self.request.user)


class CallOutcomeViewSet(BaseCallViewSet):
    serializer_class = CallOutcomeSerializer
    queryset = CallOutcome.objects.all()


class PhoneNumberViewSet(BaseCallViewSet):
    serializer_class = PhoneNumberSerializer
    queryset = PhoneNumber.objects.select_related("team")
