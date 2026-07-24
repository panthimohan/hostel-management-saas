from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from utils.models import TenantModel



class PaymentMethod(models.TextChoices):

    CASH = "CASH", "Cash"

    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"

    BANK_QR = "BANK_QR", "Bank QR"

    ESEWA = "ESEWA", "eSewa"

    KHALTI = "KHALTI", "Khalti"

    FONEPAY = "FONEPAY", "FonePay"

    CREDIT_CARD = "CREDIT_CARD", "Credit Card"

    STRIPE = "STRIPE", "Stripe"

    PAYPAL = "PAYPAL", "PayPal"




class InvoiceStatus(models.TextChoices):

    UNPAID = "UNPAID", "Unpaid"

    PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"

    PAID = "PAID", "Paid"

    OVERDUE = "OVERDUE", "Overdue"




class PaymentSubmissionStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    APPROVED = "APPROVED", "Approved"

    REJECTED = "REJECTED", "Rejected"







class RentInvoice(TenantModel):

    bed_allocation = models.ForeignKey(
        "beds.BedAllocation",
        on_delete=models.PROTECT,
        related_name="invoices"
    )


    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )


    billing_period_start = models.DateField()

    billing_period_end = models.DateField()

    due_date = models.DateField()



    rent_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    utility_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.UNPAID
    )


    notes = models.TextField(
        blank=True
    )



    class Meta:

        ordering = [
            "-due_date"
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "bed_allocation",
                    "billing_period_start",
                    "billing_period_end"
                ],
                name="unique_invoice_period"
            )

        ]



    def save(self,*args,**kwargs):

        if not self.invoice_number:

            self.invoice_number = (
                f"INV-{self.organization_id}-"
                f"{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )


        super().save(*args,**kwargs)




    @property
    def total_amount(self):

        return (
            self.rent_amount
            +
            self.security_deposit
            +
            self.utility_amount
            +
            self.late_fee
        )



    @property
    def amount_paid(self):

        return sum(
            (
                p.amount
                for p in self.payments.all()
            ),
            Decimal("0")
        )



    @property
    def outstanding_balance(self):

        return (
            self.total_amount
            -
            self.amount_paid
        )



    def refresh_status(self):

        paid = self.amount_paid


        if paid <= 0:

            status = InvoiceStatus.UNPAID


        elif paid < self.total_amount:

            status = InvoiceStatus.PARTIALLY_PAID


        else:

            status = InvoiceStatus.PAID



        if self.status != status:

            self.status = status

            self.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )






class PaymentQR(TenantModel):

    hostel = models.ForeignKey(
        "hostels.Hostel",
        on_delete=models.CASCADE,
        related_name="payment_qrs"
    )


    title = models.CharField(
        max_length=100
    )


    payment_type = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )


    qr_image = models.ImageField(
        upload_to="payment_qr/"
    )


    account_name = models.CharField(
        max_length=150,
        blank=True
    )


    account_number = models.CharField(
        max_length=100,
        blank=True
    )


    is_active = models.BooleanField(
        default=True
    )



    def clean(self):

        if self.is_active:

            count = PaymentQR.objects.filter(
                hostel=self.hostel,
                is_active=True
            ).exclude(
                id=self.id
            ).count()


            if count >= 5:

                raise ValidationError(
                    "Maximum 5 active QR codes allowed."
                )



    def save(self,*args,**kwargs):

        self.full_clean()

        super().save(*args,**kwargs)






class Payment(TenantModel):


    invoice = models.ForeignKey(
        RentInvoice,
        on_delete=models.PROTECT,
        related_name="payments"
    )


    payment_qr = models.ForeignKey(
        PaymentQR,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )


    reference_number = models.CharField(
        max_length=100,
        blank=True
    )


    paid_on = models.DateField()



    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recorded_payments"
    )


    notes = models.TextField(
        blank=True
    )



    def save(self,*args,**kwargs):

        super().save(*args,**kwargs)

        self.invoice.refresh_status()




class PaymentSubmission(TenantModel):


    invoice = models.ForeignKey(
        RentInvoice,
        on_delete=models.CASCADE,
        related_name="payment_submissions"
    )


    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payment_submissions"
    )


    payment_qr = models.ForeignKey(
        PaymentQR,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    transaction_id = models.CharField(
        max_length=150
    )


    screenshot = models.ImageField(
        upload_to="payment_submissions/"
    )


    status = models.CharField(
        max_length=20,
        choices=PaymentSubmissionStatus.choices,
        default=PaymentSubmissionStatus.PENDING
    )


    remarks = models.TextField(
        blank=True
    )


    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_submissions"
    )


    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )



    class Meta:

        ordering=[
            "-created_at"
        ]