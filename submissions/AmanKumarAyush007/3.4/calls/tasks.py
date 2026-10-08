
import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg, Count, Sum
from django.utils import timezone

from .models import CallLog


logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def notify_call_completion(self, call_log_id: int):
    """Notify a supervisor when a call is completed."""

    try:
        call = CallLog.objects.get(id=call_log_id)

        subject = f"Call Completed: {call.caller_number}"

        message = (
            f"Agent: {call.agent_name}\n"
            f"Caller: {call.caller_number}\n"
            f"Duration: {call.duration_display()}\n"
            f"Status: {call.status}\n"
            f"Notes: {call.notes}"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.SUPERVISOR_EMAIL],
            fail_silently=False,
        )

        logger.info(
            "Notification sent for call log %s",
            call_log_id,
        )

        return {
            "status": "sent",
            "call_id": call_log_id,
        }

    except CallLog.DoesNotExist:
        logger.error(
            "CallLog %s not found",
            call_log_id,
        )
        raise

    except Exception as exc:
        logger.exception(
            "Failed to send notification for call %s",
            call_log_id,
        )
        raise self.retry(exc=exc)


@shared_task
def generate_call_report(report_date=None):
    """Generate call statistics for a selected date."""

    if report_date is None:
        report_date = timezone.localdate().isoformat()

    calls = CallLog.objects.filter(
        timestamp__date=report_date
    )

    statistics = calls.aggregate(
        total_calls=Count("id"),
        total_duration=Sum("duration_secs"),
        average_duration=Avg("duration_secs"),
    )

    status_counts = {
        status: calls.filter(status=status).count()
        for status, _ in CallLog.STATUS_CHOICES
    }

    report = {
        "date": report_date,
        "total_calls": statistics["total_calls"],
        "total_duration": statistics["total_duration"] or 0,
        "average_duration": round(
            statistics["average_duration"] or 0, 2
        ),
        "status_counts": status_counts,
    }

    logger.info(
        "Generated call report for %s: %s",
        report_date,
        report,
    )

    return report




@shared_task
def send_daily_digest():
    """Email a daily summary of call activity."""

    report_date = timezone.localdate().isoformat()

    # Reuse the existing report task logic synchronously
    # inside this Celery worker.
    report = generate_call_report(report_date)

    counts = report["status_counts"]

    subject = f"Daily Call Digest - {report_date}"

    message = (
        f"Daily Call Report: {report_date}\n\n"
        f"Total Calls: {report['total_calls']}\n"
        f"Completed: {counts['completed']}\n"
        f"Missed: {counts['missed']}\n"
        f"Dropped: {counts['dropped']}\n"
        f"Voicemail: {counts['voicemail']}\n"
        f"Total Duration: {report['total_duration']} seconds\n"
        f"Average Duration: {report['average_duration']} seconds"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.SUPERVISOR_EMAIL],
        fail_silently=False,
    )

    logger.info(
        "Daily digest generated for %s",
        report_date
    )

    return {
        "status": "sent",
        "date": report_date,
        "total_calls": report["total_calls"],
    }
