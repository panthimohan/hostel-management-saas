from rest_framework import serializers

from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Organization
        fields = (
            "id", "name", "address", "owner", "owner_email",
            "subscription_plan", "status",
            "trial_ends_at", "subscription_expires_at",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "owner", "created_at", "updated_at")
