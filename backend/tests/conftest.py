import pytest
from rest_framework.test import APIClient

from apps.accounts.models import Role, User
from apps.hostels.models import Hostel
from apps.tenants.models import Organization, OrganizationStatus


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def organization_a(db):
    return Organization.objects.create(name="Sunrise Hostels", status=OrganizationStatus.ACTIVE)


@pytest.fixture
def organization_b(db):
    return Organization.objects.create(name="Blue Sky Hostels", status=OrganizationStatus.ACTIVE)


@pytest.fixture
def owner_a(db, organization_a):
    return User.objects.create_user(
        email="owner-a@example.com",
        password="StrongPassw0rd!",
        role=Role.HOSTEL_OWNER,
        organization=organization_a,
    )


@pytest.fixture
def owner_b(db, organization_b):
    return User.objects.create_user(
        email="owner-b@example.com",
        password="StrongPassw0rd!",
        role=Role.HOSTEL_OWNER,
        organization=organization_b,
    )


@pytest.fixture
def hostel_a(db, organization_a):
    return Hostel.objects.create(
        organization=organization_a,
        name="Sunrise Downtown",
        address="1 Main St",
        city="Toronto",
        country="Canada",
    )


@pytest.fixture
def hostel_b(db, organization_b):
    return Hostel.objects.create(
        organization=organization_b,
        name="Blue Sky Uptown",
        address="2 Second Ave",
        city="Vancouver",
        country="Canada",
    )


def authenticate(api_client, user, password="StrongPassw0rd!"):
    response = api_client.post(
        "/api/auth/login/", {"email": user.email, "password": password}, format="json"
    )
    assert response.status_code == 200, response.data
    access = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return response.data
