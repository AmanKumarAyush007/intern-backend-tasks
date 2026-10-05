# Exercise 3.4 — Celery Background Tasks

## 🎯 Objective

Offload heavy work to **background task queues** using Celery + Redis. In Swarelic, many operations (sending transcripts, generating reports, notifying agents) happen asynchronously — this exercise teaches you exactly how.

**Time estimate:** 5–6 hours

**Prerequisites:** Complete Exercises 3.1–3.3. Have Redis running locally.

---

## 🛠️ What You'll Build

- A Celery worker connected to Redis
- 3 background tasks: email notification, call report generation, daily summary
- A periodic task using Celery Beat
- Task status tracking via `AsyncResult`

---

## 📋 Requirements

### 1. Install Celery

```bash
pip install celery redis django-celery-beat django-celery-results
```

Add to `INSTALLED_APPS`:
```python
'django_celery_beat',
'django_celery_results',
```

### 2. Celery Configuration (`project/celery.py`)

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('calllog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

In `project/__init__.py`:
```python
from .celery import app as celery_app
__all__ = ('celery_app',)
```

In `settings.py`:
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

### 3. Task 1 — Call Completion Notification (`calls/tasks.py`)

```python
from celery import shared_task
from django.core.mail import send_mail
from .models import CallLog
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_call_completion(self, call_log_id: int):
    """
    Send an email notification when a call is marked as completed.
    Retries up to 3 times on failure with 60s delay.
    """
    try:
        call = CallLog.objects.get(id=call_log_id)
        # TODO: send_mail with:
        # subject: "Call Completed: {caller_number}"
        # message: Include agent, duration, notes
        # from_email: settings.DEFAULT_FROM_EMAIL
        # recipient_list: [settings.SUPERVISOR_EMAIL]  (add this to settings)
        logger.info(f"Notification sent for call log {call_log_id}")
        return {"status": "sent", "call_id": call_log_id}
    except CallLog.DoesNotExist:
        logger.error(f"CallLog {call_log_id} not found")
        raise
    except Exception as exc:
        logger.error(f"Failed to send notification: {exc}")
        raise self.retry(exc=exc)
```

**Trigger this task** automatically when a call's status changes to `completed`. Hook this into the API view's `perform_update()` method.

### 4. Task 2 — Generate Call Report (`calls/tasks.py`)

```python
@shared_task
def generate_call_report(agent_name: str, date_str: str):
    """
    Generate a daily call summary report for an agent.
    Returns a dict with: total_calls, completed, missed, dropped,
    avg_duration_secs, total_duration_secs.
    """
    from datetime import datetime
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # TODO: Query CallLog for the given agent and date
    # TODO: Aggregate counts by status and compute averages
    # TODO: Return the summary dict
    pass
```

### 5. Task 3 — Daily Digest (Periodic Task)

```python
@shared_task
def send_daily_digest():
    """
    Every day at 6:00 PM IST, send a summary of all call logs for the day.
    This should aggregate stats for ALL agents.
    """
    # TODO: Get today's calls, group by agent, compute stats
    # TODO: Format as a readable report string
    # TODO: Log the report (use logger.info for now, simulate email)
    pass
```

Configure this periodic task programmatically via `django_celery_beat`:
- Schedule: Daily at 18:00 (6 PM) IST
- Task: `calls.tasks.send_daily_digest`

### 6. API Endpoint for Task Status

Add an endpoint to check task status:

```
GET /api/v1/tasks/<task_id>/
```

Response:
```json
{
  "task_id": "abc-123",
  "status": "SUCCESS",  // PENDING | STARTED | SUCCESS | FAILURE | RETRY
  "result": { ... }     // the return value of the task
}
```

---

## ✅ Acceptance Criteria

- [ ] `celery -A project worker --loglevel=info` starts without errors
- [ ] Creating a completed call via API triggers `notify_call_completion` within 2 seconds
- [ ] `generate_call_report.delay("Alice", "2024-01-15")` returns a valid summary dict
- [ ] `GET /api/v1/tasks/<task_id>/` returns current task status
- [ ] Task retries on `smtplib.SMTPException` (test by setting bad email settings)
- [ ] `send_daily_digest` can be triggered manually and logs output
- [ ] `celery -A project beat` starts and schedules the daily digest

---

## 🧪 Running Celery Locally

Open **3 separate terminals**:

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A project worker --loglevel=info --concurrency=2

# Terminal 3: Celery beat scheduler (for periodic tasks)
celery -A project beat --loglevel=info
```

Test task manually:
```bash
# In Django shell
python manage.py shell
>>> from calls.tasks import generate_call_report
>>> result = generate_call_report.delay("Alice", "2024-01-15")
>>> result.id       # copy this
>>> result.status   # PENDING / SUCCESS
>>> result.get()    # blocks until done, returns value
```

---

## 💡 Hints

- Always use `.delay()` or `.apply_async()` — never call tasks directly in production
- `bind=True` gives the task access to `self` for retries
- Use `django-celery-results` so results are stored in the database (not lost on restart)
- Email won't actually send in development — use Django's console email backend:
  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
  ```

---

## 📚 References

- [Celery Official Docs](https://docs.celeryq.dev/en/stable/)
- [django-celery-beat](https://django-celery-beat.readthedocs.io/)
- [Celery Task Retries](https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying)
