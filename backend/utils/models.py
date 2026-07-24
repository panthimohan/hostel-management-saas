"""
Shared base model classes.

TenantModel is the foundation of the multi-tenant isolation guarantee:
every business table inherits organization / created_at / updated_at,
and TenantManager makes it hard to accidentally query across organizations.
"""
from django.db import models


class TenantManager(models.Manager):
    """
    Default manager for tenant-scoped models.

    Use `for_organization(org)` everywhere in views/services instead of
    the bare queryset, so cross-tenant leaks require an explicit,
    reviewable override rather than being the accidental default.
    """

    def for_organization(self, organization):
        return self.get_queryset().filter(organization=organization)


class TenantModel(models.Model):
    """
    Abstract base class for every tenant-owned table.

    Guarantees:
      - organization_id foreign key (data isolation boundary)
      - created_at / updated_at audit timestamps
    """

    organization = models.ForeignKey(
        "tenants.Organization",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantManager()

    class Meta:
        abstract = True
