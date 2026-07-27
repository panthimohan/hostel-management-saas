from django.db import transaction

from .models import Payment


@transaction.atomic
def record_manual_payment(
    *,
    invoice,
    organization,
    amount,
    method,
    paid_on,
    recorded_by,
    reference_number="",
    notes="",
    payment_qr=None,
):
    """
    Record an offline/manual payment.

    Used for:
    - Cash
    - Bank Transfer
    - eSewa (verified directly by staff)
    - Khalti (verified directly by staff)
    - Card
    """

    payment = Payment.objects.create(
        organization=organization,
        invoice=invoice,
        amount=amount,
        method=method,
        payment_qr=payment_qr,
        reference_number=reference_number,
        paid_on=paid_on,
        recorded_by=recorded_by,
        notes=notes,
    )

    invoice.refresh_status()

    return payment