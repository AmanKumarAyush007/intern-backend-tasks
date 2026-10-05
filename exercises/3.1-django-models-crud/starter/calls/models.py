"""
calls/models.py — Starter for Exercise 3.1

TODO: Complete the CallLog model as described in docs/01-django-models-crud.md
"""
from django.db import models


class CallLog(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('missed',    'Missed'),
        ('dropped',   'Dropped'),
        ('voicemail', 'Voicemail'),
    ]

    agent_name    = models.CharField(max_length=150)
    caller_number = models.CharField(max_length=20)
    duration_secs = models.PositiveIntegerField(default=0)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp     = models.DateTimeField(auto_now_add=True)
    notes         = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.agent_name} — {self.caller_number} ({self.status})"

    def duration_display(self) -> str:
        """
        Return human-readable duration string.

        Examples:
            0  seconds → "0s"
            45 seconds → "45s"
           150 seconds → "2m 30s"
          3900 seconds → "1h 5m 0s"

        TODO: Implement this method.
        """
        # YOUR CODE HERE
        pass
