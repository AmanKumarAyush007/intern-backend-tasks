
import re

from rest_framework import serializers

from .models import CallLog


class CallLogSerializer(serializers.ModelSerializer):
    """Serialize and validate call log records."""

    duration_display = serializers.SerializerMethodField()

    class Meta:
        model = CallLog
        fields = [
            'id',
            'agent_name',
            'caller_number',
            'duration_secs',
            'status',
            'timestamp',
            'notes',
            'duration_display',
        ]
        read_only_fields = [
            'id',
            'timestamp',
            'duration_display',
        ]

    def get_duration_display(self, obj):
        """Return the formatted call duration."""
        return obj.duration_display()

    def validate_duration_secs(self, value):
        """Reject negative call durations."""
        if value < 0:
            raise serializers.ValidationError(
                "Duration cannot be negative."
            )
        return value

    def validate_caller_number(self, value):
        """Allow digits, plus signs, hyphens and spaces."""
        if len(value) < 7:
            raise serializers.ValidationError(
                "Caller number must contain at least 7 characters."
            )

        if not re.fullmatch(r'[0-9+\- ]+', value):
            raise serializers.ValidationError(
                "Caller number contains invalid characters."
            )

        return value
