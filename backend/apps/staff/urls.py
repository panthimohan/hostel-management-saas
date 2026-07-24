from rest_framework.routers import DefaultRouter

from .views import StaffMemberViewSet

router = DefaultRouter()
router.register("", StaffMemberViewSet, basename="staff-member")

urlpatterns = router.urls
