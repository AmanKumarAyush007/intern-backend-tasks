
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('calls/', include('calls.urls', namespace='calls')),

    path('api/v1/', include('calls.api_urls')),

    path(
        'api/auth/register/',
        RegisterView.as_view(),
        name='register',
    ),

    path(
        'api/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain',
    ),

    path(
        'api/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    path(
        '',
        RedirectView.as_view(
            url='/calls/',
            permanent=False,
        ),
    ),
]
