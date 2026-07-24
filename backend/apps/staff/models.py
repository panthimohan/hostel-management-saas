from django.conf import settings
from django.db import models

from utils.models import TenantModel


class StaffPosition(models.TextChoices):
    MANAGER = "MANAGER", "Manager"
    RECEPTIONIST = "RECEPTIONIST", "Receptionist"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    CLEANER = "CLEANER", "Cleaner"
    SECURITY = "SECURITY", "Security"
    COOK = "COOK", "Cook"
    OTHER = "OTHER", "Other"


class StaffStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class StaffMember(TenantModel):
    """
    HR record for anyone working at a hostel. `user` is optional —
    Cleaners/Security/Cooks often don't need platform logins, while
    Managers/Receptionists/Accountants usually do (link to their User).
    """

    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, related_name="staff_members")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_record"
    )
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=20, choices=StaffPosition.choices, default=StaffPosition.OTHER)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=StaffStatus.choices, default=StaffStatus.ACTIVE)

    class Meta:
        ordering = ["full_name"]
        indexes = [models.Index(fields=["organization", "hostel", "position"])]

    def __str__(self):
        return f"{self.full_name} ({self.get_position_display()})"
