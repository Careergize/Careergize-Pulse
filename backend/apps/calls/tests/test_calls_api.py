from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.calls.models import Call, CallEvent, CallNote, CallOutcome
from apps.contacts.models import Contact
from apps.organizations.models import Organization


class CallsApiTests(TestCase):
    def setUp(self):
        self.a = Organization.objects.create(name="A", slug="calls-a")
        self.b = Organization.objects.create(name="B", slug="calls-b")
        self.user = User.objects.create_user(
            email="calls@a.test",
            password="password-123",
            name="Admin",
            organization=self.a,
            role=User.Role.COMPANY_ADMIN,
        )
        self.other = User.objects.create_user(
            email="calls@b.test",
            password="password-123",
            name="Other",
            organization=self.b,
            role=User.Role.COMPANY_ADMIN,
        )
        self.contact = Contact.objects.create(
            organization=self.a, name="Ada Lovelace", phone_number="+441234"
        )
        self.outcome = CallOutcome.objects.create(organization=self.a, name="Interested")
        self.started = timezone.now().replace(microsecond=0)
        self.call = Call.objects.create(
            organization=self.a,
            direction="inbound",
            caller_number="+441234",
            receiver_number="+449999",
            contact=self.contact,
            status="ringing",
            started_at=self.started,
            source="Website",
        )
        self.foreign = Call.objects.create(
            organization=self.b,
            direction="outbound",
            caller_number="+1",
            receiver_number="+2",
            status="failed",
            started_at=self.started,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_update_and_retrieve_call(self):
        response = self.client.post(
            "/api/v1/calls/",
            {
                "direction": "outbound",
                "caller_number": "+10",
                "receiver_number": "+20",
                "status": "ringing",
                "started_at": self.started.isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.patch(
            f"/api/v1/calls/{response.data['id']}/",
            {"status": "completed", "outcome": str(self.outcome.id)},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["outcome_name"], "Interested")

    def test_events_and_notes(self):
        event = self.client.post(
            "/api/v1/call-events/",
            {
                "call": str(self.call.id),
                "event_type": "answered",
                "timestamp": (self.started + timedelta(seconds=5)).isoformat(),
                "payload": {},
            },
            format="json",
        )
        note = self.client.post(
            "/api/v1/call-notes/",
            {"call": str(self.call.id), "text": "Requested a callback"},
            format="json",
        )
        self.assertEqual((event.status_code, note.status_code), (201, 201))
        self.assertEqual(CallEvent.objects.get().organization, self.a)
        self.assertEqual(CallNote.objects.get().author, self.user)

    def test_isolation_permissions_filters_search_and_pagination(self):
        self.assertEqual(self.client.get(f"/api/v1/calls/{self.foreign.id}/").status_code, 404)
        self.assertEqual(
            self.client.patch(
                f"/api/v1/calls/{self.foreign.id}/", {"status": "completed"}, format="json"
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.get("/api/v1/calls/?direction=inbound&status=ringing&source=Website").data[
                "count"
            ],
            1,
        )
        self.assertEqual(self.client.get("/api/v1/calls/?search=Lovela").data["count"], 1)
        self.assertEqual(self.client.get("/api/v1/calls/?search=441234").data["count"], 1)
        response = self.client.get("/api/v1/calls/")
        self.assertIn("results", response.data)

    def test_cross_tenant_relationships_rejected(self):
        foreign_outcome = CallOutcome.objects.create(organization=self.b, name="Spam")
        response = self.client.patch(
            f"/api/v1/calls/{self.call.id}/", {"outcome": str(foreign_outcome.id)}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_analyst_is_read_only(self):
        analyst = User.objects.create_user(
            email="analyst@a.test",
            password="password-123",
            name="Analyst",
            organization=self.a,
            role=User.Role.ANALYST,
        )
        self.client.force_authenticate(analyst)
        self.assertEqual(self.client.get("/api/v1/calls/").status_code, 200)
        self.assertEqual(
            self.client.patch(
                f"/api/v1/calls/{self.call.id}/", {"status": "completed"}, format="json"
            ).status_code,
            403,
        )
