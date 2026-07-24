from django.utils import timezone
from django.db import transaction

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


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
)





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









class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer


    permission_classes = [
        IsAuthenticated,
        IsPaymentViewer,
        OrganizationIsActive,
        BelongsToSameOrganization,
    ]



    def get_queryset(self):

        user = self.request.user


        qs = Payment.objects.select_related(
            "invoice",
            "payment_qr",
        )


        if user.is_superuser or user.role=="SUPER_ADMIN":

            return qs



        if user.role=="TENANT":

            return qs.filter(
                invoice__bed_allocation__tenant=user
            )


        return qs.filter(
            organization_id=user.organization_id
        )






    def perform_create(self,serializer):

        payment = serializer.save(

            organization=self.request.user.organization,

            recorded_by=self.request.user

        )


        payment.invoice.refresh_status()











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
        )



        # TENANT
        # show QR belonging to his hostel

        if user.role=="TENANT":

            return qs.filter(
                hostel__rooms__beds__allocations__tenant=user
            ).distinct()



        return qs.filter(
            organization_id=user.organization_id
        )






    def perform_create(self,serializer):

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

        user=self.request.user


        qs = PaymentSubmission.objects.select_related(
            "invoice",
            "tenant",
            "payment_qr",
        )


        if user.role=="TENANT":

            return qs.filter(
                tenant=user
            )


        return qs.filter(
            organization_id=user.organization_id
        )






    def perform_create(self,serializer):


        serializer.save(

            tenant=self.request.user,

            organization=self.request.user.organization

        )









    @transaction.atomic
    @action(
        detail=True,
        methods=["post"]
    )
    def approve(self,request,pk=None):


        submission=self.get_object()



        if submission.status != PaymentSubmissionStatus.PENDING:

            return Response(
                {
                    "detail":
                    "Already processed"
                },
                status=400
            )



        submission.status = (
            PaymentSubmissionStatus.APPROVED
        )


        submission.verified_by=request.user

        submission.verified_at=timezone.now()

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
    def reject(self,request,pk=None):


        submission=self.get_object()



        submission.status = (
            PaymentSubmissionStatus.REJECTED
        )


        submission.remarks = request.data.get(
            "remarks",
            ""
        )


        submission.verified_by=request.user

        submission.verified_at=timezone.now()

        submission.save()



        return Response({

            "message":
            "Payment rejected"

        })