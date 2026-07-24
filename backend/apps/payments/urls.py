from rest_framework.routers import DefaultRouter

from .views import (
    RentInvoiceViewSet,
    PaymentViewSet,
    PaymentQRViewSet,
    PaymentSubmissionViewSet,
)


router = DefaultRouter()


# IMPORTANT:
# Specific routes must come before empty payment route


router.register(
    "invoices",
    RentInvoiceViewSet,
    basename="rent-invoice"
)


router.register(
    "payment-qrs",
    PaymentQRViewSet,
    basename="payment-qr"
)


router.register(
    "payment-submissions",
    PaymentSubmissionViewSet,
    basename="payment-submission"
)


router.register(
    "",
    PaymentViewSet,
    basename="payment"
)


urlpatterns = router.urls