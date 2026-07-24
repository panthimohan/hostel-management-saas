from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id", "hostel", "room", "tenant", "full_name", "email", "phone",
            "preferred_check_in", "preferred_check_out", "status", "notes",
            "created_by", "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "created_by", "status", "created_at", "updated_at")

    def validate_hostel(self, hostel):
        request = self.context["request"]
        user = request.user
        if not (user.is_superuser or user.role == "SUPER_ADMIN"):
            if hostel.organization_id != user.organization_id:
                raise serializers.ValidationError("Hostel does not belong to your organization.")
        return hostel
