from rest_framework import serializers

from .models import Expense, Income


class ExpenseSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Expense
        fields = (
            "id", "hostel", "category", "category_display", "title", "note",
            "amount", "payment_method", "receipt", "incurred_on",
            "recorded_by", "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "recorded_by", "created_at", "updated_at")

    def validate(self, attrs):
        category = attrs.get("category", getattr(self.instance, "category", None))
        note = attrs.get("note", getattr(self.instance, "note", ""))
        if category == "MISCELLANEOUS" and not note:
            raise serializers.ValidationError(
                {"note": "Please describe what this miscellaneous expense was for."}
            )
        return attrs

    def validate_hostel(self, hostel):
        request = self.context["request"]
        user = request.user
        if not (user.is_superuser or user.role == "SUPER_ADMIN"):
            if hostel.organization_id != user.organization_id:
                raise serializers.ValidationError("Hostel does not belong to your organization.")
        return hostel


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = (
            "id", "hostel", "title", "amount", "payment_method",
            "received_on", "recorded_by", "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "recorded_by", "created_at", "updated_at")

    def validate_hostel(self, hostel):
        request = self.context["request"]
        user = request.user
        if not (user.is_superuser or user.role == "SUPER_ADMIN"):
            if hostel.organization_id != user.organization_id:
                raise serializers.ValidationError("Hostel does not belong to your organization.")
        return hostel
