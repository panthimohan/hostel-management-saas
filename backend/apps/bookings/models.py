from django.conf import settings
from django.db import models

from utils.models import TenantModel


class ReservationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    WAITLISTED = "WAITLISTED", "Waitlisted"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"


class Reservation(TenantModel):
    """
    Covers online booking, reservation, waiting list, confirmation, and
    cancellation. `tenant` is optional because a booking may come in
    from a prospective guest who doesn't have a platform account yet —
    full_name/email/phone capture their details either way.
    """

    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.SET_NULL, null=True, blank=True, related_name="reservations"
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservations"
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    preferred_check_in = models.DateField()
    preferred_check_out = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="reservations_created"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["organization", "hostel", "status"])]

    def __str__(self):
        return f"{self.full_name} - {self.hostel} ({self.status})"
