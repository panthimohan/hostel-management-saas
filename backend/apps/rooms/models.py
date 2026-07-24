from django.db import models

from utils.models import TenantModel


class RoomType(models.TextChoices):
    SINGLE = "SINGLE", "Single"
    DOUBLE = "DOUBLE", "Double"
    DORMITORY = "DORMITORY", "Dormitory"
    SUITE = "SUITE", "Suite"


class RoomStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    FULL = "FULL", "Full"
    MAINTENANCE = "MAINTENANCE", "Under Maintenance"
    CLOSED = "CLOSED", "Closed"


class Room(TenantModel):
    hostel = models.ForeignKey(
        "hostels.Hostel", on_delete=models.CASCADE, related_name="rooms"
    )
    room_number = models.CharField(max_length=20)
    floor = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=1)
    room_type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.SINGLE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=RoomStatus.choices, default=RoomStatus.AVAILABLE)

    class Meta:
        indexes = [models.Index(fields=["organization", "hostel", "status"])]
        constraints = [
            models.UniqueConstraint(
                fields=["hostel", "room_number"], name="unique_room_number_per_hostel"
            )
        ]

    def __str__(self):
        return f"Room {self.room_number} - {self.hostel.name}"
