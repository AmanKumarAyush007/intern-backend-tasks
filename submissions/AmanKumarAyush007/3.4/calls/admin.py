from django.contrib import admin
from .models import CallLog


@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = (
        'agent_name',
        'caller_number',
        'status',
        'duration_display',
        'timestamp',
    )

    list_filter = ('status',)

    search_fields = (
        'agent_name',
        'caller_number',
    )

    date_hierarchy = 'timestamp'