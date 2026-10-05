# Exercise 3.5 — External API Integration

## 🎯 Objective

Integrate with an **external REST API** using Python's `requests` library — with proper error handling, retries, and webhook processing. This mirrors how Swarelic integrates with telephony providers, CRM systems, and notification services.

**Time estimate:** 4–5 hours

**Prerequisites:** Complete Exercises 3.1–3.3.

---

## 🛠️ What You'll Build

- An API client class for the [JSONPlaceholder](https://jsonplaceholder.typicode.com/) mock API (simulating a CRM)
- A webhook receiver endpoint that validates and processes incoming payloads
- Rate-limit aware retries using `tenacity`
- A management command to sync data from the external API

---

## 📋 Requirements

### 1. Install Dependencies

```bash
pip install requests tenacity
```

### 2. CRM API Client (`calls/crm_client.py`)

Build a reusable client class:

```python
import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from django.conf import settings

logger = logging.getLogger(__name__)

class CRMClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            # In production this would be: 'Authorization': f'Bearer {settings.CRM_API_KEY}'
        })
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(requests.exceptions.ConnectionError),
    )
    def get_users(self) -> list[dict]:
        """Fetch all users from the CRM (simulated via JSONPlaceholder)."""
        # TODO: GET /users, return list of dicts, raise on non-2xx
        pass

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def get_user(self, user_id: int) -> dict:
        """Fetch a single user by ID."""
        # TODO: GET /users/{user_id}
        # Raise ValueError if user_id <= 0
        # Raise requests.HTTPError if 404
        pass

    def create_post(self, title: str, body: str, user_id: int) -> dict:
        """Create a new post in the CRM (simulated)."""
        # TODO: POST /posts with json payload
        # TODO: Validate: title and body non-empty, user_id > 0
        # TODO: Return parsed JSON response
        pass

    def _handle_response(self, response: requests.Response) -> dict:
        """Check for errors and parse JSON. Raise on non-2xx."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | Response: {response.text}")
            raise
        except ValueError:
            logger.error(f"Invalid JSON response: {response.text}")
            raise
```

### 3. Webhook Receiver (`calls/views.py` or `calls/webhook_views.py`)

Build an endpoint that receives incoming webhook payloads:

```
POST /api/webhooks/call-completed/
```

**Expected payload:**
```json
{
  "event": "call.completed",
  "secret": "swarelic-webhook-secret-2024",
  "data": {
    "agent_name": "Alice",
    "caller_number": "+91-9876543210",
    "duration_secs": 245,
    "status": "completed",
    "notes": "Customer satisfied"
  }
}
```

**Implementation requirements:**
- Validate the `secret` against `settings.WEBHOOK_SECRET`
- Validate the `event` field is one of: `call.completed`, `call.missed`, `call.dropped`
- If valid, create a `CallLog` record from the payload
- Return `{"status": "ok", "id": <created_id>}` with `201`
- Return `{"error": "..."}` with `400` or `403` on invalid requests
- Use `@csrf_exempt` since webhooks come from external services

### 4. Management Command — Sync Users (`calls/management/commands/sync_crm_users.py`)

```python
from django.core.management.base import BaseCommand
from calls.crm_client import CRMClient

class Command(BaseCommand):
    help = 'Sync users from CRM API into the database'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Print what would be synced without saving')

    def handle(self, *args, **options):
        client = CRMClient()
        # TODO: Fetch all users from CRM
        # TODO: For each user, create or update the local User model
        # TODO: Log: "Created X new users, updated Y existing users"
        # TODO: If --dry-run, only print; don't save
        pass
```

Run with:
```bash
python manage.py sync_crm_users
python manage.py sync_crm_users --dry-run
```

---

## ✅ Acceptance Criteria

- [ ] `CRMClient().get_users()` returns a list of dicts with keys `id`, `name`, `email`
- [ ] `CRMClient().get_user(0)` raises `ValueError`
- [ ] `CRMClient().get_user(999)` raises `requests.HTTPError` (404)
- [ ] `POST /api/webhooks/call-completed/` with valid payload returns `201` and creates a `CallLog`
- [ ] Webhook with wrong `secret` returns `403`
- [ ] Webhook with unknown `event` returns `400`
- [ ] `python manage.py sync_crm_users` runs and prints a completion message
- [ ] `python manage.py sync_crm_users --dry-run` prints users without saving

---

## 🧪 Testing the Webhook

```bash
# Valid webhook
curl -X POST http://localhost:8000/api/webhooks/call-completed/ \
  -H "Content-Type: application/json" \
  -d '{
    "event": "call.completed",
    "secret": "swarelic-webhook-secret-2024",
    "data": {
      "agent_name": "Bob",
      "caller_number": "+91-9000000000",
      "duration_secs": 120,
      "status": "completed"
    }
  }'

# Invalid secret
curl -X POST http://localhost:8000/api/webhooks/call-completed/ \
  -H "Content-Type: application/json" \
  -d '{"event": "call.completed", "secret": "wrong", "data": {}}'
```

---

## 💡 Hints

- Use `requests.Session()` for connection pooling — more efficient than individual requests
- `tenacity` is more flexible than `requests`'s built-in retry mechanisms
- Always validate webhook secrets to prevent spoofed payloads
- Management commands are great for one-off or scheduled data sync operations
- Use `response.raise_for_status()` — never manually check `response.status_code == 200`

---

## 📚 References

- [Requests Library Docs](https://requests.readthedocs.io/)
- [Tenacity Retry Library](https://tenacity.readthedocs.io/)
- [Django Management Commands](https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)
