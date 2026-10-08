
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from accounts.permissions import (
    IsAgent,
    IsSupervisor,
    IsAdminUser,
)
from .models import CallLog
from .serializers import CallLogSerializer


class CallLogViewSet(viewsets.ModelViewSet):
    """Provide role-based access to call logs."""

    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    filterset_fields = ['status', 'agent_name']
    search_fields = ['agent_name', 'caller_number', 'notes']
    ordering_fields = ['timestamp', 'duration_secs']
    ordering = ['-timestamp']

    def get_permissions(self):
        """Return permissions according to the requested action."""
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsSupervisor]
        else:
            permission_classes = [IsAgent]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Restrict agents to their own call logs."""
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.role == 'agent':
            return queryset.filter(agent_name=user.username)

        return queryset

    def perform_create(self, serializer):
        """Assign the authenticated agent's name to new records."""
        user = self.request.user

        if user.role == 'agent':
            serializer.save(agent_name=user.username)
        else:
            serializer.save()
