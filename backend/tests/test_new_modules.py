import datetime

import pytest

from apps.accounts.models import Role, User
from apps.beds.models import Bed, BedAllocation
from apps.payments.models import RentInvoice
from apps.rooms.models import Room
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db


@pytest.fixture
def bed_allocation_a(db, organization_a, hostel_a):
    room = Room.objects.create(organization=organization_a, hostel=hostel_a, room_number="301", price="200.00")
    bed = Bed.objects.create(organization=organization_a, room=room, bed_number="A")
    tenant = User.objects.create_user(
        email="renter@example.com", password="StrongPassw0rd!", role=Role.TENANT, organization=organization_a
    )
    return BedAllocation.objects.create(
        organization=organization_a, bed=bed, tenant=tenant, check_in_date=datetime.date(2026, 1, 1)
    )


def test_tenant_can_file_complaint_and_only_sees_their_own(api_client, organization_a, hostel_a):
    tenant_1 = User.objects.create_user(
        email="t1@example.com", password="StrongPassw0rd!", role=Role.TENANT, organization=organization_a
    )
    tenant_2 = User.objects.create_user(
        email="t2@example.com", password="StrongPassw0rd!", role=Role.TENANT, organization=organization_a
    )

    authenticate(api_client, tenant_1)
    response = api_client.post(
        "/api/complaints/",
        {"hostel": hostel_a.id, "category": "WATER", "description": "No hot water since Monday."},
        format="json",
    )
    assert response.status_code == 201

    authenticate(api_client, tenant_2)
    response = api_client.get("/api/complaints/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 0


def test_owner_can_see_and_resolve_complaints(api_client, owner_a, organization_a, hostel_a):
    tenant = User.objects.create_user(
        email="t3@example.com", password="StrongPassw0rd!", role=Role.TENANT, organization=organization_a
    )
    authenticate(api_client, tenant)
    created = api_client.post(
        "/api/complaints/",
        {"hostel": hostel_a.id, "category": "MAINTENANCE", "description": "Leaking pipe."},
        format="json",
    )
    complaint_id = created.data["id"]

    authenticate(api_client, owner_a)
    response = api_client.get("/api/complaints/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1

    response = api_client.post(f"/api/complaints/{complaint_id}/resolve/")
    assert response.status_code == 200
    assert response.data["status"] == "RESOLVED"


def test_recording_full_payment_marks_invoice_paid(api_client, owner_a, bed_allocation_a):
    authenticate(api_client, owner_a)
    invoice_res = api_client.post(
        "/api/payments/invoices/",
        {
            "bed_allocation": bed_allocation_a.id,
            "billing_period_start": "2026-03-01",
            "billing_period_end": "2026-03-31",
            "due_date": "2026-03-05",
            "rent_amount": "200.00",
        },
        format="json",
    )
    assert invoice_res.status_code == 201
    invoice_id = invoice_res.data["id"]
    assert invoice_res.data["status"] == "UNPAID"

    payment_res = api_client.post(
        "/api/payments/",
        {"invoice": invoice_id, "amount": "200.00", "method": "CASH", "paid_on": "2026-03-04"},
        format="json",
    )
    assert payment_res.status_code == 201

    invoice = RentInvoice.objects.get(id=invoice_id)
    assert invoice.status == "PAID"
    assert invoice.outstanding_balance == 0


def test_partial_payment_marks_invoice_partially_paid(api_client, owner_a, bed_allocation_a):
    authenticate(api_client, owner_a)
    invoice_res = api_client.post(
        "/api/payments/invoices/",
        {
            "bed_allocation": bed_allocation_a.id,
            "billing_period_start": "2026-04-01",
            "billing_period_end": "2026-04-30",
            "due_date": "2026-04-05",
            "rent_amount": "200.00",
        },
        format="json",
    )
    invoice_id = invoice_res.data["id"]

    api_client.post(
        "/api/payments/",
        {"invoice": invoice_id, "amount": "50.00", "method": "CASH", "paid_on": "2026-04-04"},
        format="json",
    )

    invoice = RentInvoice.objects.get(id=invoice_id)
    assert invoice.status == "PARTIALLY_PAID"
    assert invoice.outstanding_balance == 150


def test_receptionist_role_can_manage_reservations_but_not_expenses(api_client, organization_a):
    receptionist = User.objects.create_user(
        email="reception@example.com", password="StrongPassw0rd!",
        role=Role.RECEPTIONIST, organization=organization_a,
    )
    authenticate(api_client, receptionist)

    response = api_client.get("/api/reservations/")
    assert response.status_code == 200

    response = api_client.get("/api/expenses/")
    assert response.status_code == 403
