from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "subscription_plan",
        "status",
        "created_at",
    )

    list_filter = (
        "subscription_plan",
        "status",
    )

    search_fields = (
        "name",
        "owner__email",
    )

    actions = [
        "approve_organizations",
        "suspend_organizations",
    ]

    @admin.action(description="Approve selected organizations")
    def approve_organizations(self, request, queryset):
        queryset.update(status="ACTIVE")

    @admin.action(description="Suspend selected organizations")
    def suspend_organizations(self, request, queryset):
        queryset.update(status="SUSPENDED")