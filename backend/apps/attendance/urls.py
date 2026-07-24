from rest_framework.routers import DefaultRouter

from .views import AttendanceRecordViewSet

router = DefaultRouter()
router.register("", AttendanceRecordViewSet, basename="attendance")

urlpatterns = router.urls
