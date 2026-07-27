from rest_framework import serializers

from .models import (
    Payment,
    RentInvoice,
    PaymentQR,
    PaymentSubmission,
    PaymentMethod,
)



class RentInvoiceSerializer(serializers.ModelSerializer):

    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    amount_paid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    outstanding_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    tenant_email = serializers.EmailField(
        source="bed_allocation.tenant.email",
        read_only=True
    )


    class Meta:

        model = RentInvoice

        fields = [
            "id",
            "invoice_number",
            "bed_allocation",
            "tenant_email",

            "billing_period_start",
            "billing_period_end",
            "due_date",

            "rent_amount",
            "security_deposit",
            "utility_amount",
            "late_fee",

            "total_amount",
            "amount_paid",
            "outstanding_balance",

            "status",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "invoice_number",
            "status",
            "created_at",
            "updated_at",
        ]



# keep everything above RentInvoiceSerializer the same


class PaymentQRSerializer(serializers.ModelSerializer):

    hostel_name = serializers.CharField(
        source="hostel.name",
        read_only=True
    )


    qr_image_url = serializers.SerializerMethodField()


    class Meta:

        model = PaymentQR

        fields = [

            "id",

            "hostel",
            "hostel_name",

            "title",

            "payment_type",

            "qr_image",
            "qr_image_url",

            "account_name",
            "account_number",

            "is_active",

            "created_at",
            "updated_at",

        ]


        read_only_fields = [

            "id",
            "created_at",
            "updated_at",

        ]


    def get_qr_image_url(self, obj):

        request = self.context.get("request")

        if obj.qr_image:

            url = obj.qr_image.url

            if request:
                return request.build_absolute_uri(url)

            return url

        return None



class PaymentSerializer(serializers.ModelSerializer):


    invoice_number = serializers.CharField(
        source="invoice.invoice_number",
        read_only=True
    )


    tenant_name = serializers.SerializerMethodField()


    tenant_email = serializers.EmailField(
        source="invoice.bed_allocation.tenant.email",
        read_only=True
    )


    tenant_phone = serializers.CharField(
        source="invoice.bed_allocation.tenant.phone",
        read_only=True
    )


    room_number = serializers.CharField(
        source="invoice.bed_allocation.bed.room.room_number",
        read_only=True
    )


    bed_number = serializers.CharField(
        source="invoice.bed_allocation.bed.bed_number",
        read_only=True
    )



    def get_tenant_name(self, obj):

        tenant = obj.invoice.bed_allocation.tenant

        name = f"{tenant.first_name} {tenant.last_name}".strip()

        return name if name else tenant.email



    class Meta:

        model = Payment

        fields = [

            "id",

            "receipt_number",

            "invoice",

            "invoice_number",

            "tenant_name",
            "tenant_email",
            "tenant_phone",

            "room_number",
            "bed_number",

            "amount",

            "method",

            "payment_qr",

            "reference_number",

            "paid_on",

            "recorded_by",

            "notes",

            "created_at",

        ]


        read_only_fields = [

            "id",

            "receipt_number",

            "invoice_number",

            "tenant_name",
            "tenant_email",
            "tenant_phone",

            "room_number",
            "bed_number",

            "recorded_by",

            "created_at",

        ]







class PaymentSubmissionSerializer(serializers.ModelSerializer):


    tenant_email = serializers.EmailField(
        source="tenant.email",
        read_only=True
    )


    invoice_number = serializers.CharField(
        source="invoice.invoice_number",
        read_only=True
    )


    payment_method = serializers.CharField(
        source="payment_qr.payment_type",
        read_only=True
    )


    qr_title = serializers.CharField(
        source="payment_qr.title",
        read_only=True
    )



    class Meta:

        model = PaymentSubmission


        fields = [

            "id",

            "invoice",
            "invoice_number",

            "tenant",
            "tenant_email",

            "payment_qr",
            "payment_method",
            "qr_title",

            "amount",

            "transaction_id",

            "screenshot",

            "status",

            "remarks",

            "verified_by",

            "verified_at",

            "created_at",

        ]


        read_only_fields = [

            "id",

            "tenant",

            "status",

            "verified_by",

            "verified_at",

            "created_at",

        ]





class ManualPaymentSerializer(serializers.Serializer):

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    method = serializers.ChoiceField(
        choices=PaymentMethod.choices
    )


    paid_on = serializers.DateField(
        required=False
    )


    reference_number = serializers.CharField(
        required=False,
        allow_blank=True
    )


    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )