from django.conf import settings
from django.db import models

from utils.models import TenantModel


class Visitor(TenantModel):
    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, related_name="visitors")
    tenant_visited = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="visitors_received"
    )
    visitor_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    purpose = models.CharField(max_length=255, blank=True)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="visitors_logged"
    )

    class Meta:
        ordering = ["-entry_time"]
        indexes = [models.Index(fields=["organization", "hostel", "entry_time"])]

    def __str__(self):
        return f"{self.visitor_name} visiting {self.tenant_visited}"
