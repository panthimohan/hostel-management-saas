from django.db import models


class SubscriptionPlan(models.TextChoices):
    BASIC = "BASIC", "Basic"
    PROFESSIONAL = "PROFESSIONAL", "Professional"
    ENTERPRISE = "ENTERPRISE", "Enterprise"


class OrganizationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending Approval"
    ACTIVE = "ACTIVE", "Active"
    SUSPENDED = "SUSPENDED", "Suspended"
    CANCELLED = "CANCELLED", "Cancelled"


class Organization(models.Model):
    """
    The tenant record. One Organization == one hostel business
    (which may itself operate multiple physical Hostel locations).
    """

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True)
    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_organizations",
    )
    subscription_plan = models.CharField(
        max_length=20, choices=SubscriptionPlan.choices, default=SubscriptionPlan.BASIC
    )
    status = models.CharField(
        max_length=20, choices=OrganizationStatus.choices, default=OrganizationStatus.PENDING
    )
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
