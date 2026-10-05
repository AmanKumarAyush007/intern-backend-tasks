# Exercise 3.3 — Authentication & Permissions

## 🎯 Objective

Secure the API from Exercise 3.2 using **JWT-based authentication** and **role-based permissions**. In Swarelic, agents, supervisors, and admins have different access levels — this exercise teaches you to enforce that.

**Time estimate:** 4–5 hours

**Prerequisite:** Complete Exercises 3.1 and 3.2.

---

## 🛠️ What You'll Build

- JWT authentication using `djangorestframework-simplejwt`
- A custom `User` model with a `role` field (`agent`, `supervisor`, `admin`)
- Role-based permission classes
- Protected API endpoints with proper 401/403 responses
- Token refresh mechanism

---

## 📋 Requirements

### 1. Install SimpleJWT

```bash
pip install djangorestframework-simplejwt
```

Add to `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### 2. Custom User Model (`accounts/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('agent',      'Agent'),
        ('supervisor', 'Supervisor'),
        ('admin',      'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')

    def is_supervisor_or_above(self):
        return self.role in ('supervisor', 'admin')

    def __str__(self):
        return f"{self.username} ({self.role})"
```

Set in `settings.py`:
```python
AUTH_USER_MODEL = 'accounts.User'
```

### 3. Permission Classes (`accounts/permissions.py`)

Create three custom permissions:

```python
from rest_framework.permissions import BasePermission

class IsAgent(BasePermission):
    """Allow any authenticated user (agents, supervisors, admins)."""
    def has_permission(self, request, view):
        # TODO: return True if user is authenticated
        pass

class IsSupervisor(BasePermission):
    """Allow only supervisors and admins."""
    def has_permission(self, request, view):
        # TODO: check user.is_supervisor_or_above()
        pass

class IsAdminUser(BasePermission):
    """Allow only admin-role users."""
    def has_permission(self, request, view):
        # TODO: check user.role == 'admin'
        pass
```

### 4. JWT Auth URLs (`project/urls.py`)

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
]
```

### 5. Registration View (`accounts/views.py`)

Create a `RegisterView` that:
- Accepts `username`, `email`, `password`, `role`
- Validates password length >= 8 characters
- Does **not** allow self-assigning `admin` role (that must be done by existing admin)
- Returns the created user's data + JWT tokens on success

### 6. Apply Permissions to Call Log API

Update `CallLogViewSet` with role-based access:

| Action | Required Role |
|--------|--------------|
| `list`, `retrieve` | Agent or above |
| `create` | Agent or above |
| `update`, `partial_update` | Supervisor or above |
| `destroy` | Admin only |

Implement `get_permissions()` in the ViewSet to apply different permissions per action.

### 7. Ownership Filter

Agents should **only see their own call logs** (where `agent_name` matches their username).
Supervisors and Admins can see all logs.

Override `get_queryset()` in `CallLogViewSet` to enforce this.

---

## 🔗 API Endpoints

| Method | URL | Auth Required | Description |
|--------|-----|--------------|-------------|
| `POST` | `/api/auth/register/` | No | Register new user |
| `POST` | `/api/auth/token/` | No | Get access + refresh tokens |
| `POST` | `/api/auth/token/refresh/` | No | Refresh access token |
| `GET` | `/api/v1/call-logs/` | Yes (Agent+) | List own logs (agent) / all (supervisor+) |
| `DELETE` | `/api/v1/call-logs/<id>/` | Yes (Admin) | Delete a log |

---

## ✅ Acceptance Criteria

- [ ] `POST /api/auth/token/` with valid credentials returns `access` and `refresh` tokens
- [ ] `GET /api/v1/call-logs/` without token returns `401 Unauthorized`
- [ ] Agent can only see their own call logs
- [ ] Agent `PATCH /api/v1/call-logs/<id>/` returns `403 Forbidden`
- [ ] Supervisor can update any call log
- [ ] `DELETE` by a supervisor returns `403 Forbidden`
- [ ] Admin can delete any call log
- [ ] Registration with `role=admin` returns `400 Bad Request`
- [ ] Registration with weak password (< 8 chars) returns `400 Bad Request`

---

## 🧪 Testing Flow

```bash
# 1. Register an agent
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "securepass123", "email": "alice@test.com", "role": "agent"}'

# 2. Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "securepass123"}'

# 3. Use token (copy from step 2)
curl http://localhost:8000/api/v1/call-logs/ \
  -H "Authorization: Bearer <access_token>"

# 4. Try to delete (should fail for agent)
curl -X DELETE http://localhost:8000/api/v1/call-logs/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 💡 Hints

- Set `AUTH_USER_MODEL` **before** your first `migrate` — changing it later is complex
- Use `get_permissions()` returning a list of instantiated permission objects
- The `has_object_permission()` method is called per-object for retrieve/update/delete
- Test all roles: create 3 users in the shell — one per role

---

## 📚 References

- [SimpleJWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Custom Permissions](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions)
- [Custom User Model](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model)
