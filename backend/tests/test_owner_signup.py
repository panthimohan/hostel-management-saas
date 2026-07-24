import pytest

from apps.accounts.models import Role, User
from apps.tenants.models import Organization, OrganizationStatus
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db


@pytest.fixture
def super_admin(db):
    return User.objects.create_superuser(
        email="admin@platform.com", password="StrongPassw0rd!"
    )


def test_owner_signup_creates_pending_organization(api_client):
    response = api_client.post(
        "/api/auth/owner-signup/",
        {
            "organization_name": "Sunset Hostels",
            "email": "new-owner@example.com",
            "password": "StrongPassw0rd!",
            "phone": "+1-555-0100",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["status"] == OrganizationStatus.PENDING

    org = Organization.objects.get(name="Sunset Hostels")
    assert org.status == OrganizationStatus.PENDING
    owner = User.objects.get(email="new-owner@example.com")
    assert owner.role == Role.HOSTEL_OWNER
    assert owner.organization_id == org.id
    assert org.owner_id == owner.id


def test_owner_signup_rejects_duplicate_org_name(api_client, organization_a):
    response = api_client.post(
        "/api/auth/owner-signup/",
        {
            "organization_name": organization_a.name,
            "email": "someone@example.com",
            "password": "StrongPassw0rd!",
        },
        format="json",
    )
    assert response.status_code == 400


def test_new_owner_can_log_in_but_cannot_manage_hostels_while_pending(api_client):
    api_client.post(
        "/api/auth/owner-signup/",
        {
            "organization_name": "Pending Hostels Co",
            "email": "pending-owner@example.com",
            "password": "StrongPassw0rd!",
        },
        format="json",
    )
    owner = User.objects.get(email="pending-owner@example.com")
    authenticate(api_client, owner)

    response = api_client.get("/api/hostels/")
    assert response.status_code == 403
    assert "not yet active" in str(response.data).lower()


def test_super_admin_can_approve_organization_and_unlock_access(api_client, super_admin):
    signup = api_client.post(
        "/api/auth/owner-signup/",
        {
            "organization_name": "Harbor View Hostels",
            "email": "harbor-owner@example.com",
            "password": "StrongPassw0rd!",
        },
        format="json",
    )
    org_id = signup.data["organization_id"]
    owner = User.objects.get(email="harbor-owner@example.com")

    # Super Admin approves
    authenticate(api_client, super_admin, password="StrongPassw0rd!")
    response = api_client.post(f"/api/tenants/organizations/{org_id}/approve/")
    assert response.status_code == 200
    assert response.data["status"] == OrganizationStatus.ACTIVE

    # Owner logs back in and can now manage hostels
    owner_client_auth = authenticate(api_client, owner)
    assert owner_client_auth["user"]["email"] == owner.email

    response = api_client.get("/api/hostels/")
    assert response.status_code == 200


def test_non_super_admin_cannot_approve_organizations(api_client, owner_a, organization_b):
    authenticate(api_client, owner_a)
    response = api_client.post(f"/api/tenants/organizations/{organization_b.id}/approve/")
    assert response.status_code == 403


def test_super_admin_can_suspend_an_active_organization(api_client, super_admin, organization_a, owner_a):
    organization_a.status = OrganizationStatus.ACTIVE
    organization_a.save(update_fields=["status"])

    authenticate(api_client, super_admin, password="StrongPassw0rd!")
    response = api_client.post(f"/api/tenants/organizations/{organization_a.id}/suspend/")
    assert response.status_code == 200
    assert response.data["status"] == OrganizationStatus.SUSPENDED

    authenticate(api_client, owner_a)
    response = api_client.get("/api/hostels/")
    assert response.status_code == 403
