from rest_framework import serializers

from .models import Bed, BedAllocation


class BedSerializer(serializers.ModelSerializer):

    room_number = serializers.CharField(
        source="room.room_number",
        read_only=True
    )

    hostel_name = serializers.CharField(
        source="room.hostel.name",
        read_only=True
    )


    class Meta:
        model = Bed

        fields = (
            "id",
            "room",
            "room_number",
            "hostel_name",
            "bed_number",
            "status",
            "organization",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "organization",
            "created_at",
            "updated_at",
        )


class BedAllocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BedAllocation

        fields = (
            "id",
            "bed",
            "tenant",
            "check_in_date",
            "check_out_date",
            "agreement_document",
            "organization",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "organization",
            "created_at",
            "updated_at",
        )


    def validate(self, data):

        tenant = data.get("tenant")

        # During checkout/update tenant may not be sent
        if self.instance and tenant is None:
            tenant = self.instance.tenant


        if tenant is None:
            raise serializers.ValidationError(
                {
                    "tenant":"Tenant is required."
                }
            )


        # Ensure only tenant users receive beds
        if tenant.role != "TENANT":
            raise serializers.ValidationError(
                {
                    "tenant":"Only TENANT users can be assigned beds."
                }
            )


        bed = data.get("bed")

        if self.instance and bed is None:
            bed = self.instance.bed


        active_allocation = BedAllocation.objects.filter(
            bed=bed,
            check_out_date__isnull=True
        )

        # Prevent tenant from having multiple active beds
        tenant_active_allocation = BedAllocation.objects.filter(
            tenant=tenant,
            check_out_date__isnull=True
        )

        if self.instance:
            tenant_active_allocation = tenant_active_allocation.exclude(
                id=self.instance.id
            )


        if tenant_active_allocation.exists():
            raise serializers.ValidationError(
                {
                    "tenant":
                    "This tenant already has an active bed allocation."
                }
            )


        if self.instance:
            active_allocation = active_allocation.exclude(
                id=self.instance.id
            )


        if active_allocation.exists():
            raise serializers.ValidationError(
                {
                    "bed":"This bed is already occupied."
                }
            )


        return data