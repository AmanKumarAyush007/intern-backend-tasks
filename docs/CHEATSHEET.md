# Django & DRF Cheatsheet

## Models

```python
# Basic model
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'My Models'

    def __str__(self):
        return self.name
```

## Migrations

```bash
python manage.py makemigrations         # Create migration
python manage.py migrate                # Apply migration
python manage.py showmigrations         # List migrations
python manage.py sqlmigrate app 0001    # Show SQL for a migration
python manage.py migrate app zero       # Rollback all migrations for an app
```

## ORM Queries

```python
# Fetch
MyModel.objects.all()
MyModel.objects.filter(name='Alice')
MyModel.objects.exclude(is_active=False)
MyModel.objects.get(id=1)             # raises DoesNotExist if not found
MyModel.objects.first()
MyModel.objects.last()

# Create
obj = MyModel.objects.create(name='Alice')
obj = MyModel(name='Bob'); obj.save()

# Update
MyModel.objects.filter(id=1).update(name='Charlie')
obj.name = 'Dave'; obj.save()

# Delete
MyModel.objects.filter(id=1).delete()
obj.delete()

# Aggregation
from django.db.models import Count, Avg, Sum, Max, Min
MyModel.objects.aggregate(total=Count('id'))
MyModel.objects.values('status').annotate(count=Count('id'))

# Q objects (complex queries)
from django.db.models import Q
MyModel.objects.filter(Q(name='Alice') | Q(name='Bob'))
MyModel.objects.filter(Q(is_active=True) & ~Q(name='Eve'))

# Related objects
author.books.all()           # reverse FK lookup
Book.objects.select_related('author')    # JOIN (FK)
Book.objects.prefetch_related('tags')    # prefetch (M2M)
```

## Class-Based Views

```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

class BookListView(ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        return qs.filter(title__icontains=q) if q else qs

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'published']
    success_url = reverse_lazy('books:list')
```

## DRF Serializers

```python
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'published']
        read_only_fields = ['id']

    def get_author_name(self, obj):
        return obj.author.get_full_name()

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title too short")
        return value

    def validate(self, attrs):
        # Cross-field validation
        if attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError("end_date must be after start_date")
        return attrs
```

## DRF ViewSets

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Custom action: POST /api/books/{id}/publish/"""
        book = self.get_object()
        book.is_published = True
        book.save()
        return Response({'status': 'published'})

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
```

## JWT Auth

```python
# Get token
POST /api/auth/token/
{"username": "alice", "password": "secret"}
→ {"access": "...", "refresh": "..."}

# Use token
GET /api/endpoint/
Authorization: Bearer <access_token>

# Refresh token
POST /api/auth/token/refresh/
{"refresh": "..."}
→ {"access": "..."}
```

## Common HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth token |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limiting |
| 500 | Internal Server Error | Unexpected server error |

## Celery Quick Reference

```python
# Define task
@shared_task
def add(x, y):
    return x + y

# Call task
add.delay(4, 4)                          # fire and forget
result = add.apply_async((4, 4), countdown=10)  # with delay
result.get(timeout=5)                    # wait for result
result.status                            # PENDING / SUCCESS / FAILURE

# Start worker
celery -A project worker --loglevel=info

# Start beat scheduler
celery -A project beat --loglevel=info
```
