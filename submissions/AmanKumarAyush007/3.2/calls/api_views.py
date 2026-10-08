
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import CallLog
from .serializers import CallLogSerializer


class CallLogViewSet(viewsets.ModelViewSet):
    """Provide CRUD API operations for call logs."""

    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    filterset_fields = ['status', 'agent_name']

    search_fields = [
        'agent_name',
        'caller_number',
        'notes',
    ]

    ordering_fields = [
        'timestamp',
        'duration_secs',
    ]

    ordering = ['-timestamp']
