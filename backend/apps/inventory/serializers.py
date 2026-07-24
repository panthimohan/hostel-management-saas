from rest_framework import serializers

from .models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = InventoryItem
        fields = (
            "id", "hostel", "name", "category", "category_display", "quantity",
            "condition", "purchase_date", "notes",
            "organization", "created_at", "updated_at",
        )
        read_only_fields = ("id", "organization", "created_at", "updated_at")
