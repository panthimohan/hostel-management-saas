from django.conf import settings
from django.db import models

from utils.models import TenantModel


class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"
    LEAVE = "LEAVE", "Leave"
    LATE = "LATE", "Late Entry"


class AttendanceRecord(TenantModel):
    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, related_name="attendance_records")
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    note = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="attendance_marked"
    )

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["organization", "hostel", "date"])]
        constraints = [
            models.UniqueConstraint(fields=["tenant", "date"], name="unique_attendance_per_tenant_per_day")
        ]

    def __str__(self):
        return f"{self.tenant} - {self.date} ({self.status})"
