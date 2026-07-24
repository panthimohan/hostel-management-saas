"""
Role-based access control permission classes for DRF.

Usage:
    permission_classes = [IsAuthenticated, IsHostelOwnerOrManager]
"""
from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    """Base class: subclass and set `allowed_roles`."""

    allowed_roles: tuple[str, ...] = ()
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role in self.allowed_roles)
        )

class IsPaymentViewer(HasRole):
    """
    Users who can view payment information.
    """
    allowed_roles = (
        "SUPER_ADMIN",
        "HOSTEL_OWNER",
        "HOSTEL_MANAGER",
        "ACCOUNTANT",
        "TENANT",
    )


class IsSuperAdmin(HasRole):
    allowed_roles = ("SUPER_ADMIN",)


class IsHostelOwner(HasRole):
    allowed_roles = ("SUPER_ADMIN", "HOSTEL_OWNER")


class IsHostelOwnerOrManager(HasRole):
    allowed_roles = ("SUPER_ADMIN", "HOSTEL_OWNER", "HOSTEL_MANAGER")


class IsFrontDeskStaff(HasRole):
    """Owner/Manager/Receptionist — for bookings, visitors, attendance."""
    allowed_roles = ("SUPER_ADMIN", "HOSTEL_OWNER", "HOSTEL_MANAGER", "RECEPTIONIST")


class IsAccountingStaff(HasRole):
    """Owner/Manager/Accountant — for rent invoices, payments, expenses."""
    allowed_roles = ("SUPER_ADMIN", "HOSTEL_OWNER", "HOSTEL_MANAGER", "ACCOUNTANT")


class IsTenantUser(HasRole):
    allowed_roles = ("TENANT",)


class OrganizationIsActive(BasePermission):
    """
    Blocks hostel/room/bed management until a Super Admin has approved
    the user's Organization (status=ACTIVE). Super Admins always pass,
    since they may need to inspect a PENDING organization's data.
    """

    message = (
        "Your organization is not yet active. It may be pending Super Admin "
        "approval, suspended, or cancelled. Contact support if this seems wrong."
    )

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser or user.role == "SUPER_ADMIN":
            return True

        # Allow tenants to access their own payment information
        if user.role == "TENANT":
            return True

        organization = user.organization

        return bool(
            organization and organization.status == "ACTIVE"
        )


class BelongsToSameOrganization(BasePermission):
    """
    Object-level check: the object's organization must match the
    requesting user's organization (Super Admins bypass this).
    """

    message = "This resource belongs to a different organization."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role == "SUPER_ADMIN":
            return True
        obj_org_id = getattr(obj, "organization_id", None)
        return obj_org_id is not None and obj_org_id == user.organization_id
