from django.conf import settings
from django.db import models

from utils.models import TenantModel


class BedStatus(models.TextChoices):
    VACANT = "VACANT", "Vacant"
    OCCUPIED = "OCCUPIED", "Occupied"
    RESERVED = "RESERVED", "Reserved"
    MAINTENANCE = "MAINTENANCE", "Under Maintenance"


class Bed(TenantModel):
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name="beds")
    bed_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=BedStatus.choices, default=BedStatus.VACANT)

    class Meta:
        indexes = [models.Index(fields=["organization", "room", "status"])]
        constraints = [
            models.UniqueConstraint(fields=["room", "bed_number"], name="unique_bed_number_per_room")
        ]

    def __str__(self):
        return f"Bed {self.bed_number} - {self.room}"


class BedAllocation(TenantModel):
    """Links a tenant (User with role=TENANT) to a bed for a stay period."""

    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name="allocations")
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bed_allocations"
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    agreement_document = models.FileField(upload_to="agreements/", null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["organization", "tenant"])]

    def __str__(self):
        return f"{self.tenant} -> {self.bed} ({self.check_in_date})"
