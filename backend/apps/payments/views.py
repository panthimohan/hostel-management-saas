from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from datetime import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from permissions.roles import (
    BelongsToSameOrganization,
    IsPaymentViewer,
    OrganizationIsActive,
)


from .models import (
    Payment,
    RentInvoice,
    PaymentQR,
    PaymentSubmission,
    PaymentSubmissionStatus,
)


from .serializers import (
    PaymentSerializer,
    RentInvoiceSerializer,
    PaymentQRSerializer,
    PaymentSubmissionSerializer,
    ManualPaymentSerializer,
)


from .services import record_manual_payment




class RentInvoiceViewSet(viewsets.ModelViewSet):

    serializer_class = RentInvoiceSerializer

    permission_classes = [
        IsAuthenticated,
        IsPaymentViewer,
        OrganizationIsActive,
        BelongsToSameOrganization,
    ]


    def get_queryset(self):

        user = self.request.user

        qs = RentInvoice.objects.select_related(
            "bed_allocation",
            "bed_allocation__tenant",
        )


        if user.is_superuser or user.role == "SUPER_ADMIN":
            return qs


        if user.role == "TENANT":
            return qs.filter(
                bed_allocation__tenant=user
            )


        return qs.filter(
            organization_id=user.organization_id
        )



    @action(
        detail=True,
        methods=["post"],
        url_path="record-payment"
    )
    def record_payment(self, request, pk=None):

        invoice = self.get_object()


        serializer = ManualPaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        data = serializer.validated_data


        payment = record_manual_payment(

            invoice=invoice,

            organization=invoice.organization,

            amount=data["amount"],

            method=data["method"],

            paid_on=data.get(
                "paid_on",
                timezone.now().date()
            ),

            recorded_by=request.user,

            reference_number=data.get(
                "reference_number",
                ""
            ),

            notes=data.get(
                "notes",
                ""
            ),
        )


        return Response(
            {
                "message": "Payment recorded successfully",

                "payment_id": payment.id,

                "receipt_number": payment.receipt_number,

                "amount": payment.amount,

                "method": payment.method,

                "paid_on": payment.paid_on,

                "invoice_id": invoice.id,

                "invoice_status": invoice.status,
            },
            status=status.HTTP_201_CREATED
        )





class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.all()

    serializer_class = PaymentSerializer


    def perform_create(self, serializer):

        user = self.request.user

        serializer.save(
            recorded_by=user,
            organization=user.organization
        )



    def get_queryset(self):

        user = self.request.user


        qs = Payment.objects.select_related(
            "invoice",
            "payment_qr",
        ).order_by(
            "-created_at"
        )


        if user.is_superuser or user.role == "SUPER_ADMIN":
            return qs


        if user.role == "TENANT":

            return qs.filter(
                invoice__bed_allocation__tenant=user
            )


        return qs.filter(
            organization_id=user.organization_id
        )



    @action(
        detail=False,
        methods=["get"],
        url_path="dashboard-summary"
    )
    def dashboard_summary(self, request):

        user = request.user


        invoices = RentInvoice.objects.filter(
            organization_id=user.organization_id
        )


        payments = Payment.objects.filter(
            organization_id=user.organization_id
        )


        total_due = invoices.aggregate(
            total=Sum("total_amount")
        )["total"] or 0


        collected = payments.aggregate(
            total=Sum("amount")
        )["total"] or 0


        pending = invoices.exclude(
            status="PAID"
        ).aggregate(
            total=Sum("outstanding_balance")
        )["total"] or 0


        start_month = date.today().replace(
            day=1
        )


        this_month = payments.filter(
            paid_on__gte=start_month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
class PaymentQRViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentQRSerializer

    permission_classes = [
        IsAuthenticated,
        IsPaymentViewer,
        OrganizationIsActive,
        BelongsToSameOrganization,
    ]


    def get_queryset(self):

        user = self.request.user

        qs = PaymentQR.objects.select_related(
            "hostel"
        ).filter(
            is_active=True
        ).order_by(
            "-created_at"
        )


        if user.role == "TENANT":

            return qs.filter(
                hostel__rooms__beds__allocations__tenant=user
            ).distinct()


        return qs.filter(
            organization_id=user.organization_id
        )



    def perform_create(self, serializer):

        serializer.save(
            organization=self.request.user.organization
        )









class PaymentSubmissionViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSubmissionSerializer


    permission_classes = [

        IsAuthenticated,
        OrganizationIsActive,

    ]



    def get_queryset(self):

        user = self.request.user


        qs = PaymentSubmission.objects.select_related(
            "invoice",
            "tenant",
            "payment_qr",
        ).order_by(
            "-created_at"
        )


        if user.role == "TENANT":

            return qs.filter(
                tenant=user
            )


        return qs.filter(
            organization_id=user.organization_id
        )




    def perform_create(self, serializer):

        serializer.save(

            tenant=self.request.user,

            organization=self.request.user.organization

        )






    @transaction.atomic
    @action(
        detail=True,
        methods=["post"]
    )
    def approve(self, request, pk=None):

        submission = self.get_object()


        if submission.status != PaymentSubmissionStatus.PENDING:

            return Response(
                {
                    "detail":
                    "Already processed"
                },
                status=400
            )



        submission.status = PaymentSubmissionStatus.APPROVED

        submission.verified_by = request.user

        submission.verified_at = timezone.now()

        submission.save()



        payment = Payment.objects.create(

            organization=submission.organization,

            invoice=submission.invoice,

            amount=submission.amount,

            method=(
                submission.payment_qr.payment_type
                if submission.payment_qr
                else "BANK_QR"
            ),

            payment_qr=submission.payment_qr,

            reference_number=submission.transaction_id,

            paid_on=timezone.now().date(),

            recorded_by=request.user,

            notes="Approved tenant payment"

        )



        submission.invoice.refresh_status()



        return Response({

            "message":
            "Payment approved",

            "payment_id":
            payment.id,

            "status":
            submission.invoice.status

        })






    @action(
        detail=True,
        methods=["post"]
    )
    def reject(self, request, pk=None):

        submission = self.get_object()



        submission.status = PaymentSubmissionStatus.REJECTED


        submission.remarks = request.data.get(
            "remarks",
            ""
        )


        submission.verified_by = request.user

        submission.verified_at = timezone.now()

        submission.save()



        return Response({

            "message":
            "Payment rejected"

        })