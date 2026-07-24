from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import BedAllocationViewSet, BedViewSet, MyAllocationView

router = DefaultRouter()
router.register("allocations", BedAllocationViewSet, basename="bed-allocation")
router.register("", BedViewSet, basename="bed")

urlpatterns = [
    path("my-room/", MyAllocationView.as_view(), name="my-room"),
] + router.urls
