from rest_framework import serializers

from .models import StaffMember


class StaffMemberSerializer(serializers.ModelSerializer):
    position_display = serializers.CharField(source="get_position_display", read_only=True)

    class Meta:
        model = StaffMember
        fields = (
            "id", "hostel", "user", "full_name", "position", "position_display",
            "phone", "email", "salary", "hire_date", "status",
            "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "created_at", "updated_at")
