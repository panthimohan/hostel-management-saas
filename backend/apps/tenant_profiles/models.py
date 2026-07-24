from django.conf import settings
from django.db import models

from utils.models import TenantModel


class IdentificationType(models.TextChoices):
    NATIONAL_ID = "NATIONAL_ID", "National ID"
    CITIZENSHIP = "CITIZENSHIP", "Citizenship Certificate"
    PASSPORT = "PASSPORT", "Passport"
    DRIVING_LICENSE = "DRIVING_LICENSE", "Driving License"
    STUDENT_ID = "STUDENT_ID", "Student ID"
    WORK_PERMIT = "WORK_PERMIT", "Work Permit"


class TenantProfile(TenantModel):
    """
    Extended personal/KYC information for a User with role=TENANT.
    Room/bed assignment and check-in/out dates live on BedAllocation
    (apps.beds) rather than here, to avoid duplicating that state.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tenant_profile"
    )
    photo = models.ImageField(upload_to="tenant_photos/", null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=500, blank=True)

    identification_type = models.CharField(
        max_length=20, choices=IdentificationType.choices, blank=True
    )
    identification_number = models.CharField(max_length=100, blank=True)
    identification_document_front = models.ImageField(
        upload_to="tenant_identification/", null=True, blank=True
    )
    identification_document_back = models.ImageField(
        upload_to="tenant_identification/", null=True, blank=True
    )

    university = models.CharField(max_length=255, blank=True)
    student_id = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [models.Index(fields=["organization", "user"])]

    def __str__(self):
        return f"Profile: {self.user.email}"
