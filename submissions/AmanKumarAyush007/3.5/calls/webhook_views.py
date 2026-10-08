
import json
import logging
from hmac import compare_digest

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CallLog


logger = logging.getLogger(__name__)

ALLOWED_EVENTS = {
    "call.completed": "completed",
    "call.missed": "missed",
    "call.dropped": "dropped",
}


@csrf_exempt
def call_completed_webhook(request):
    """Receive and validate incoming call events."""

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON payload"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "Expected a JSON object"},
            status=400,
        )

    provided_secret = payload.get("secret")

    if (
        not isinstance(provided_secret, str)
        or not compare_digest(
            provided_secret,
            settings.WEBHOOK_SECRET,
        )
    ):
        logger.warning("Rejected webhook: invalid secret")
        return JsonResponse(
            {"error": "Invalid webhook secret"},
            status=403,
        )

    event = payload.get("event")

    if event not in ALLOWED_EVENTS:
        return JsonResponse(
            {"error": "Unsupported event"},
            status=400,
        )

    data = payload.get("data")

    if not isinstance(data, dict):
        return JsonResponse(
            {"error": "Invalid call data"},
            status=400,
        )

    agent_name = data.get("agent_name")
    caller_number = data.get("caller_number")
    duration_secs = data.get("duration_secs", 0)
    status_value = data.get("status")

    if (
        not isinstance(agent_name, str)
        or not agent_name.strip()
        or not isinstance(caller_number, str)
        or not caller_number.strip()
        or not isinstance(duration_secs, int)
        or isinstance(duration_secs, bool)
        or duration_secs < 0
        or status_value != ALLOWED_EVENTS[event]
    ):
        return JsonResponse(
            {"error": "Invalid call fields"},
            status=400,
        )

    if len(agent_name) > 150 or len(caller_number) > 20:
        return JsonResponse(
            {"error": "Call field exceeds maximum length"},
            status=400,
        )

    notes = data.get("notes", "")

    if not isinstance(notes, str):
        return JsonResponse(
            {"error": "Notes must be a string"},
            status=400,
        )

    call = CallLog.objects.create(
        agent_name=agent_name,
        caller_number=caller_number,
        duration_secs=duration_secs,
        status=status_value,
        notes=notes,
    )

    logger.info("Webhook created call log %s", call.id)

    return JsonResponse(
        {"status": "ok", "id": call.id},
        status=201,
    )
