from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calls/', include('calls.urls', namespace='calls')),
    path('', RedirectView.as_view(url='/calls/', permanent=False)),
]
