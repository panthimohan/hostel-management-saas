from rest_framework import serializers

from .models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    tenant_email = serializers.EmailField(source="tenant.email", read_only=True)
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Complaint
        fields = (
            "id", "hostel", "tenant", "tenant_email", "category", "category_display",
            "description", "status", "assigned_to", "resolved_at",
            "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "tenant", "status", "resolved_at", "created_at", "updated_at")
