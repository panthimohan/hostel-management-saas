from rest_framework import serializers

from apps.hostels.models import Hostel

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id", "hostel", "room_number", "floor", "capacity",
            "room_type", "price", "status",
            "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "created_at", "updated_at")

    def validate_hostel(self, hostel: Hostel):
        request = self.context["request"]
        user = request.user
        if not (user.is_superuser or user.role == "SUPER_ADMIN"):
            if hostel.organization_id != user.organization_id:
                raise serializers.ValidationError("Hostel does not belong to your organization.")
        return hostel
