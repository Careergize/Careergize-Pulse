from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.teams.models import Agent, Team


class FoundationApiTests(TestCase):
    def setUp(self):
        self.org_a = Organization.objects.create(name="Org A", slug="org-a")
        self.org_b = Organization.objects.create(name="Org B", slug="org-b")
        self.admin_a = User.objects.create_user(
            email="admin-a@example.com",
            password="correct-pass-123",
            name="Admin A",
            organization=self.org_a,
            role=User.Role.COMPANY_ADMIN,
        )
        self.manager_a = User.objects.create_user(
            email="manager-a@example.com",
            password="correct-pass-123",
            name="Manager A",
            organization=self.org_a,
            role=User.Role.MANAGER,
        )
        self.agent_a = User.objects.create_user(
            email="agent-a@example.com",
            password="correct-pass-123",
            name="Agent A",
            organization=self.org_a,
            role=User.Role.AGENT,
        )
        self.admin_b = User.objects.create_user(
            email="admin-b@example.com",
            password="correct-pass-123",
            name="Admin B",
            organization=self.org_b,
            role=User.Role.COMPANY_ADMIN,
        )
        self.team_a = Team.objects.create(
            organization=self.org_a, name="Team A", manager=self.manager_a
        )
        self.team_b = Team.objects.create(
            organization=self.org_b, name="Team B", manager=self.admin_b
        )
        self.client = APIClient()

    def test_login_current_user_and_logout(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.admin_a.email, "password": "correct-pass-123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 200)
        self.assertEqual(self.client.post("/api/v1/auth/logout/").status_code, 204)
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 403)

    def test_invalid_credentials(self):
        response = self.client.post(
            "/api/v1/auth/login/", {"email": self.admin_a.email, "password": "wrong"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["code"], "invalid_credentials")

    def test_unauthorized_api_access(self):
        self.assertEqual(self.client.get("/api/v1/teams/").status_code, 403)

    def test_cross_tenant_ids_are_not_visible_or_mutable(self):
        self.client.force_authenticate(self.admin_a)
        self.assertEqual(self.client.get(f"/api/v1/teams/{self.team_b.id}/").status_code, 404)
        self.assertEqual(
            self.client.patch(
                f"/api/v1/teams/{self.team_b.id}/", {"name": "Hijacked"}, format="json"
            ).status_code,
            404,
        )
        self.assertEqual(self.client.get(f"/api/v1/users/{self.admin_b.id}/").status_code, 404)
        response = self.client.post(
            "/api/v1/agents/",
            {"user": str(self.admin_b.id), "team": str(self.team_a.id)},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_role_permissions(self):
        self.client.force_authenticate(self.manager_a)
        self.assertEqual(self.client.get("/api/v1/teams/").status_code, 200)
        self.assertEqual(
            self.client.post("/api/v1/teams/", {"name": "Nope"}, format="json").status_code, 403
        )
        self.assertEqual(self.client.get("/api/v1/users/").status_code, 403)
        self.client.force_authenticate(self.agent_a)
        self.assertEqual(self.client.get("/api/v1/agents/").status_code, 403)

    def test_company_admin_manages_team_and_agent_with_audit(self):
        self.client.force_authenticate(self.admin_a)
        team_response = self.client.post(
            "/api/v1/teams/", {"name": "New Team", "manager": str(self.manager_a.id)}, format="json"
        )
        self.assertEqual(team_response.status_code, 201)
        agent_response = self.client.post(
            "/api/v1/agents/",
            {"user": str(self.agent_a.id), "team": team_response.data["id"], "extension": "101"},
            format="json",
        )
        self.assertEqual(agent_response.status_code, 201)
        agent = Agent.objects.get(pk=agent_response.data["id"])
        self.assertEqual(agent.organization, self.org_a)
        self.assertEqual(self.org_a.auditlog_set.count(), 2)
