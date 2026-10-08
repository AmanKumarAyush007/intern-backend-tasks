"""
calls/views.py — Starter for Exercise 3.1

TODO: Implement all 5 class-based views as described in the exercise guide.
"""
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import CallLog


class CallLogListView(ListView):
    model = CallLog
    template_name = 'calls/call_log_list.html'
    context_object_name = 'call_logs'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')

        if status:
            queryset = queryset.filter(status=status)

        return queryset


class CallLogDetailView(DetailView):
    model = CallLog
    template_name = 'calls/call_log_detail.html'
    context_object_name = 'call_log'


class CallLogCreateView(CreateView):
    model = CallLog
    template_name = 'calls/call_log_form.html'
    fields = ['agent_name', 'caller_number', 'duration_secs', 'status', 'notes']
    success_url = reverse_lazy('calls:list')

    # TODO: Add form validation — duration_secs must be >= 0


class CallLogUpdateView(UpdateView):
    model = CallLog
    template_name = 'calls/call_log_form.html'
    fields = ['agent_name', 'caller_number', 'duration_secs', 'status', 'notes']
    success_url = reverse_lazy('calls:list')


class CallLogDeleteView(DeleteView):
    model = CallLog
    template_name = 'calls/call_log_confirm_delete.html'
    success_url = reverse_lazy('calls:list')
