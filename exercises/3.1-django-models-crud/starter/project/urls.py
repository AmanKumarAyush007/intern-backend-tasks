from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calls/', include('calls.urls', namespace='calls')),
    path('', admin.site.urls),  # Redirect root to admin for convenience
]
