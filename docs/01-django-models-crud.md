# Exercise 3.1 — Django Models & CRUD

## 🎯 Objective

Build a **Call Log Management System** using Django's ORM, admin panel, and class-based views. This exercise mirrors a core feature of the Swarelic platform: tracking and managing call records.

**Time estimate:** 3–4 hours

---

## 📖 Background

In the Swarelic platform, every call made through the system is recorded and stored. This exercise has you build the data layer for such a system — models, migrations, CRUD views, and the Django admin interface.

---

## 🛠️ What You'll Build

A Django web application with:
- A `CallLog` model with fields: agent, caller number, duration, status, timestamp, notes
- Full CRUD via Django admin + manual views
- A list view showing all call logs with filtering by status
- A detail view showing individual call info
- Form validation on the create/edit views

---

## 📋 Requirements

### 1. Model Definition (`calls/models.py`)

Create a `CallLog` model with **exactly** these fields:

```python
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

    def duration_display(self):
        """Return human-readable duration string, e.g. '2m 30s'"""
        # TODO: implement this
        pass
```

### 2. Migrations

```bash
python manage.py makemigrations calls
python manage.py migrate
```

### 3. Admin Registration (`calls/admin.py`)

Register `CallLog` in admin with:
- `list_display`: `agent_name`, `caller_number`, `status`, `duration_display`, `timestamp`
- `list_filter`: `status`
- `search_fields`: `agent_name`, `caller_number`
- `date_hierarchy`: `timestamp`

### 4. Views (`calls/views.py`)

Implement **class-based views**:

| View | URL | Description |
|------|-----|-------------|
| `CallLogListView` | `/calls/` | List all logs; support `?status=` query param filter |
| `CallLogDetailView` | `/calls/<int:pk>/` | Show single call log |
| `CallLogCreateView` | `/calls/create/` | Form to create new log |
| `CallLogUpdateView` | `/calls/<int:pk>/edit/` | Edit existing log |
| `CallLogDeleteView` | `/calls/<int:pk>/delete/` | Delete with confirmation |

### 5. Templates

Create templates in `calls/templates/calls/`:
- `call_log_list.html` — table with calls, filter dropdown
- `call_log_detail.html` — individual call card
- `call_log_form.html` — shared create/edit form
- `call_log_confirm_delete.html` — delete confirmation page

### 6. `duration_display()` Method

Implement the method to return:
- `"0s"` for 0 seconds
- `"45s"` for 45 seconds
- `"2m 30s"` for 150 seconds
- `"1h 5m 0s"` for 3900 seconds

---

## ✅ Acceptance Criteria

- [ ] `python manage.py migrate` runs without errors
- [ ] Superuser can log into Django admin and create/edit/delete `CallLog` entries
- [ ] `/calls/` shows all call logs in a table
- [ ] `/calls/?status=missed` filters to only missed calls
- [ ] `/calls/create/` form validates: agent_name is required, duration_secs must be >= 0
- [ ] `/calls/<pk>/edit/` pre-populates existing data
- [ ] `/calls/<pk>/delete/` asks for confirmation before deleting
- [ ] `duration_display()` passes all test cases in `verify.py`
- [ ] No hardcoded data — all data comes from the database

---

## 🧪 Running Tests

```bash
# Run the built-in Django tests
python manage.py test calls

# Run verifier
python ../../../scripts/verify.py --exercise 3.1 --user <your-username>
```

---

## 💡 Hints

- Use `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` from `django.views.generic`
- For filtering in `CallLogListView`, override `get_queryset()`
- Use `success_url = reverse_lazy('calls:list')` in Create/Update/Delete views
- Don't forget `{% csrf_token %}` in your forms!
- The `auto_now_add=True` field cannot be edited — exclude it from your form fields

---

## 📚 References

- [Django ORM Documentation](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Class-based views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/)
- [Django Admin](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/)
