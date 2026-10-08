
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import CallLog


class CallLogPermissionTests(TestCase):
    """Test role-based permissions for call log endpoints."""

    def setUp(self):
        """Create test users and call records."""
        User = get_user_model()

        self.agent = User.objects.create_user(
            username="alice",
            password="TestPass123!",
            role="agent",
        )

        self.supervisor = User.objects.create_user(
            username="bob",
            password="TestPass123!",
            role="supervisor",
        )

        self.admin = User.objects.create_user(
            username="charlie",
            password="TestPass123!",
            role="admin",
        )

        self.call = CallLog.objects.create(
            agent_name="alice",
            caller_number="+919876543210",
            duration_secs=150,
            status="completed",
        )

        self.client = APIClient()

    def authenticate(self, user):
        """Authenticate the client with a JWT access token."""
        from rest_framework_simplejwt.tokens import RefreshToken

        token = RefreshToken.for_user(user).access_token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_unauthenticated_access(self):
        """Anonymous requests must be rejected."""
        response = self.client.get("/api/v1/call-logs/")
        self.assertEqual(response.status_code, 401)

    def test_agent_can_view_own_calls(self):
        """Agents can retrieve their own calls."""
        self.authenticate(self.agent)

        response = self.client.get("/api/v1/call-logs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_agent_cannot_update(self):
        """Agents cannot modify existing calls."""
        self.authenticate(self.agent)

        response = self.client.patch(
            f"/api/v1/call-logs/{self.call.id}/",
            {"notes": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_supervisor_can_update(self):
        """Supervisors can update call records."""
        self.authenticate(self.supervisor)

        response = self.client.patch(
            f"/api/v1/call-logs/{self.call.id}/",
            {"notes": "Supervisor updated"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_supervisor_cannot_delete(self):
        """Supervisors cannot delete call records."""
        self.authenticate(self.supervisor)

        response = self.client.delete(
            f"/api/v1/call-logs/{self.call.id}/"
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete(self):
        """Admins can delete call records."""
        self.authenticate(self.admin)

        response = self.client.delete(
            f"/api/v1/call-logs/{self.call.id}/"
        )
        self.assertEqual(response.status_code, 204)

    def test_agent_cannot_view_other_agents_calls(self):
        """Agents must not see another agent's records."""
        CallLog.objects.create(
            agent_name="bob",
            caller_number="+919876543211",
            duration_secs=60,
            status="missed",
        )

        self.authenticate(self.agent)

        response = self.client.get("/api/v1/call-logs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
