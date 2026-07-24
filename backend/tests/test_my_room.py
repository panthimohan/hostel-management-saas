import datetime

import pytest

from apps.accounts.models import Role, User
from apps.beds.models import Bed, BedAllocation
from apps.rooms.models import Room
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db


def test_tenant_sees_their_current_room(api_client, organization_a, hostel_a):
    room = Room.objects.create(
        organization=organization_a, hostel=hostel_a, room_number="101",
        capacity=2, price="300.00",
    )
    bed = Bed.objects.create(organization=organization_a, room=room, bed_number="A")
    tenant = User.objects.create_user(
        email="tenant-x@example.com", password="StrongPassw0rd!",
        role=Role.TENANT, organization=organization_a,
    )
    BedAllocation.objects.create(
        organization=organization_a, bed=bed, tenant=tenant,
        check_in_date=datetime.date(2026, 1, 1),
    )

    authenticate(api_client, tenant)
    response = api_client.get("/api/beds/my-room/")
    assert response.status_code == 200
    assert response.data["current"]["room_number"] == "101"
    assert response.data["current"]["hostel_name"] == hostel_a.name


def test_owner_cannot_use_tenant_only_endpoint(api_client, owner_a):
    authenticate(api_client, owner_a)
    response = api_client.get("/api/beds/my-room/")
    assert response.status_code == 403
