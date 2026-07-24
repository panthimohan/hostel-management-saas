from rest_framework import serializers

from .models import Hostel


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = (
            "id", "name", "address", "city", "country",
            "registration_number", "license_number",
            "contact_phone", "contact_email",
            "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "created_at", "updated_at")
