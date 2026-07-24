from rest_framework import serializers

from .models import AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    tenant_email = serializers.EmailField(source="tenant.email", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = (
            "id", "hostel", "tenant", "tenant_email", "date", "status", "note",
            "marked_by", "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "marked_by", "created_at", "updated_at")
