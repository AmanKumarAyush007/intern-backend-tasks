
from rest_framework.routers import DefaultRouter

from .api_views import CallLogViewSet


router = DefaultRouter()

router.register(
    r'call-logs',
    CallLogViewSet,
    basename='calllog'
)

urlpatterns = router.urls
