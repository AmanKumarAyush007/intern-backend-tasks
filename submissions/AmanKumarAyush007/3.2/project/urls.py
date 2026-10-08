
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'calls/',
        include('calls.urls', namespace='calls')
    ),

    path(
        'api/v1/',
        include('calls.api_urls')
    ),

    path(
        '',
        RedirectView.as_view(
            url='/calls/',
            permanent=False
        )
    ),
]
