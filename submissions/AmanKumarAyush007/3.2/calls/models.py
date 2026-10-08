
"""Call log model for Exercise 3.1."""

from django.db import models


class CallLog(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('dropped', 'Dropped'),
        ('voicemail', 'Voicemail'),
    ]

    agent_name = models.CharField(max_length=150)
    caller_number = models.CharField(max_length=20)
    duration_secs = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """Return a readable representation of the call."""
        return f"{self.agent_name} — {self.caller_number} ({self.status})"

    def duration_display(self) -> str:
        """Return the call duration in a human-readable format."""
        seconds = self.duration_secs

        if seconds == 0:
            return "0s"

        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"

        if minutes > 0:
            return f"{minutes}m {seconds}s"

        return f"{seconds}s"
