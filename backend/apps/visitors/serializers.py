from rest_framework import serializers

from .models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    tenant_visited_email = serializers.EmailField(source="tenant_visited.email", read_only=True)

    class Meta:
        model = Visitor
        fields = (
            "id", "hostel", "tenant_visited", "tenant_visited_email", "visitor_name",
            "phone", "purpose", "entry_time", "exit_time",
            "logged_by", "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "logged_by", "created_at", "updated_at")
