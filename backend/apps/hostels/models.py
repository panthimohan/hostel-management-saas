from django.db import models

from utils.models import TenantModel


class Hostel(TenantModel):
    """A physical hostel location owned by an Organization."""

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    registration_number = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["organization", "city"])]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"], name="unique_hostel_name_per_org"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.city})"
