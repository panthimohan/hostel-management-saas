from rest_framework.routers import DefaultRouter

from .views import TenantProfileViewSet

router = DefaultRouter()
router.register("", TenantProfileViewSet, basename="tenant-profile")

urlpatterns = router.urls
