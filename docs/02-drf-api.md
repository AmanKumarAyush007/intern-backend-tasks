# Exercise 3.2 — Django REST Framework (DRF) API

## 🎯 Objective

Expose the `CallLog` data from Exercise 3.1 as a **RESTful JSON API** using Django REST Framework. This is the foundation of how Swarelic's frontend and mobile clients communicate with the backend.

**Time estimate:** 4–5 hours

**Prerequisite:** Complete Exercise 3.1 first.

---

## 🛠️ What You'll Build

A fully-functional REST API with:
- Serializers for `CallLog` with field validation
- A `ModelViewSet` with full CRUD
- Router-based URL configuration
- Pagination, filtering, and ordering
- Proper HTTP status codes and error responses

---

## 📋 Requirements

### 1. Install DRF

```bash
pip install djangorestframework django-filter
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
]
```

### 2. Serializer (`calls/serializers.py`)

Create a `CallLogSerializer` using `ModelSerializer`:

```python
from rest_framework import serializers
from .models import CallLog

class CallLogSerializer(serializers.ModelSerializer):
    duration_display = serializers.SerializerMethodField()

    class Meta:
        model = CallLog
        fields = ['id', 'agent_name', 'caller_number', 'duration_secs',
                  'status', 'timestamp', 'notes', 'duration_display']
        read_only_fields = ['id', 'timestamp', 'duration_display']

    def get_duration_display(self, obj):
        # TODO: call obj.duration_display()
        pass

    def validate_duration_secs(self, value):
        # TODO: raise ValidationError if value < 0
        pass

    def validate_caller_number(self, value):
        # TODO: ensure it contains only digits, +, -, spaces; min 7 chars
        pass
```

### 3. ViewSet (`calls/api_views.py`)

```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CallLog
from .serializers import CallLogSerializer

class CallLogViewSet(viewsets.ModelViewSet):
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'agent_name']
    search_fields = ['agent_name', 'caller_number', 'notes']
    ordering_fields = ['timestamp', 'duration_secs']
    ordering = ['-timestamp']
```

### 4. URL Configuration (`calls/api_urls.py`)

```python
from rest_framework.routers import DefaultRouter
from .api_views import CallLogViewSet

router = DefaultRouter()
router.register(r'call-logs', CallLogViewSet, basename='calllog')

urlpatterns = router.urls
```

Include in `project/urls.py`:
```python
path('api/v1/', include('calls.api_urls')),
```

### 5. Pagination

Add to `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

---

## 🔗 API Endpoints (Expected)

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/v1/call-logs/` | List all (paginated) |
| `POST` | `/api/v1/call-logs/` | Create new call log |
| `GET` | `/api/v1/call-logs/<id>/` | Retrieve single |
| `PUT` | `/api/v1/call-logs/<id>/` | Full update |
| `PATCH` | `/api/v1/call-logs/<id>/` | Partial update |
| `DELETE` | `/api/v1/call-logs/<id>/` | Delete |
| `GET` | `/api/v1/call-logs/?status=missed` | Filter by status |
| `GET` | `/api/v1/call-logs/?ordering=-duration_secs` | Order by duration |
| `GET` | `/api/v1/call-logs/?search=John` | Full-text search |

---

## ✅ Acceptance Criteria

- [ ] `GET /api/v1/call-logs/` returns JSON with `count`, `next`, `previous`, `results` keys
- [ ] `POST /api/v1/call-logs/` with valid data creates a record and returns `201 Created`
- [ ] `POST` with `duration_secs: -5` returns `400 Bad Request` with a validation error message
- [ ] `POST` with `caller_number: "abc"` (too short) returns `400 Bad Request`
- [ ] `GET /api/v1/call-logs/?status=completed` returns only completed calls
- [ ] `GET /api/v1/call-logs/?search=John` searches agent_name and caller_number
- [ ] `DELETE /api/v1/call-logs/<id>/` returns `204 No Content`
- [ ] `GET /api/v1/call-logs/<invalid-id>/` returns `404 Not Found`
- [ ] The `duration_display` field is present in all responses

---

## 🧪 Testing with curl / HTTPie

```bash
# List all call logs
curl http://localhost:8000/api/v1/call-logs/

# Create a new call log
curl -X POST http://localhost:8000/api/v1/call-logs/ \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "Alice", "caller_number": "+91-9876543210", "duration_secs": 180, "status": "completed"}'

# Filter by status
curl "http://localhost:8000/api/v1/call-logs/?status=missed"

# Update a record
curl -X PATCH http://localhost:8000/api/v1/call-logs/1/ \
  -H "Content-Type: application/json" \
  -d '{"notes": "Customer requested callback"}'
```

---

## 💡 Hints

- The `DefaultRouter` automatically creates a browsable API at `/api/v1/`
- Test your API using the **DRF Browsable API** at `http://localhost:8000/api/v1/call-logs/`
- Use `SerializerMethodField` for computed/read-only fields
- `validate_<fieldname>` methods are the idiomatic DRF way to validate individual fields

---

## 📚 References

- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
