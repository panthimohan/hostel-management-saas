from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.accounts.urls")),
    path("tenants/", include("apps.tenants.urls")),
    path("hostels/", include("apps.hostels.urls")),
    path("rooms/", include("apps.rooms.urls")),
    path("beds/", include("apps.beds.urls")),
    path("expenses/", include("apps.expenses.urls")),
    path("tenant-profiles/", include("apps.tenant_profiles.urls")),
    path("reservations/", include("apps.bookings.urls")),
    path("payments/", include("apps.payments.urls")),
    path("attendance/", include("apps.attendance.urls")),
    path("visitors/", include("apps.visitors.urls")),
    path("complaints/", include("apps.complaints.urls")),
    path("staff/", include("apps.staff.urls")),
    path("inventory/", include("apps.inventory.urls")),
]
