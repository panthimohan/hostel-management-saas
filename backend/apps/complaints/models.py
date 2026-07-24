from django.conf import settings
from django.db import models

from utils.models import TenantModel


class ComplaintCategory(models.TextChoices):
    WATER = "WATER", "Water"
    ELECTRICITY = "ELECTRICITY", "Electricity"
    INTERNET = "INTERNET", "Internet"
    CLEANING = "CLEANING", "Cleaning"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    OTHER = "OTHER", "Other"


class ComplaintStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    RESOLVED = "RESOLVED", "Resolved"


class Complaint(TenantModel):
    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, related_name="complaints")
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints_filed"
    )
    category = models.CharField(max_length=20, choices=ComplaintCategory.choices, default=ComplaintCategory.OTHER)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default=ComplaintStatus.PENDING)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="complaints_assigned",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["organization", "hostel", "status"])]

    def __str__(self):
        return f"{self.get_category_display()} complaint by {self.tenant}"
