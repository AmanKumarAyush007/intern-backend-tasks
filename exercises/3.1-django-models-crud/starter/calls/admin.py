"""
calls/admin.py — Starter for Exercise 3.1

TODO: Register the CallLog model with the admin site.
See docs/01-django-models-crud.md for the required list_display, list_filter, etc.
"""
from django.contrib import admin
from .models import CallLog


# TODO: Create a CallLogAdmin class and register it
# @admin.register(CallLog)
# class CallLogAdmin(admin.ModelAdmin):
#     ...

admin.site.register(CallLog)  # Basic registration — enhance this!
