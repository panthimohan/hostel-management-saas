import pytest

from apps.rooms.models import Room
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db


def test_owner_can_list_own_hostels_only(api_client, owner_a, owner_b, hostel_a, hostel_b):
    authenticate(api_client, owner_a)
    response = api_client.get("/api/hostels/")
    assert response.status_code == 200
    names = [h["name"] for h in response.data["results"]]
    assert hostel_a.name in names
    assert hostel_b.name not in names


def test_owner_cannot_read_other_orgs_hostel_by_id(api_client, owner_a, hostel_b):
    authenticate(api_client, owner_a)
    response = api_client.get(f"/api/hostels/{hostel_b.id}/")
    # Not in queryset at all -> 404, never leaks existence via 403
    assert response.status_code == 404


def test_owner_cannot_create_room_under_other_orgs_hostel(api_client, owner_a, hostel_b):
    authenticate(api_client, owner_a)
    response = api_client.post(
        "/api/rooms/",
        {
            "hostel": hostel_b.id,
            "room_number": "101",
            "floor": 1,
            "capacity": 2,
            "room_type": "DOUBLE",
            "price": "100.00",
        },
        format="json",
    )
    assert response.status_code == 400
    assert "does not belong" in str(response.data).lower()


def test_room_created_by_owner_is_scoped_to_their_org(api_client, owner_a, hostel_a, organization_a):
    authenticate(api_client, owner_a)
    response = api_client.post(
        "/api/rooms/",
        {
            "hostel": hostel_a.id,
            "room_number": "201",
            "floor": 2,
            "capacity": 1,
            "room_type": "SINGLE",
            "price": "50.00",
        },
        format="json",
    )
    assert response.status_code == 201
    room = Room.objects.get(id=response.data["id"])
    assert room.organization_id == organization_a.id


def test_tenant_role_cannot_manage_hostels(api_client, db, organization_a):
    from apps.accounts.models import Role, User

    tenant_user = User.objects.create_user(
        email="tenant@example.com",
        password="StrongPassw0rd!",
        role=Role.TENANT,
        organization=organization_a,
    )
    authenticate(api_client, tenant_user)
    response = api_client.get("/api/hostels/")
    assert response.status_code == 403
