import pytest

from tests.conftest import authenticate

pytestmark = pytest.mark.django_db


def test_login_success_returns_access_and_refresh(api_client, owner_a):
    data = authenticate(api_client, owner_a)
    assert "access" in data
    assert "refresh" in data
    assert data["user"]["email"] == owner_a.email


def test_login_wrong_password_fails(api_client, owner_a):
    response = api_client.post(
        "/api/auth/login/",
        {"email": owner_a.email, "password": "wrong-password"},
        format="json",
    )
    assert response.status_code == 401


def test_account_locks_after_repeated_failed_logins(api_client, owner_a):
    for _ in range(5):
        api_client.post(
            "/api/auth/login/",
            {"email": owner_a.email, "password": "wrong-password"},
            format="json",
        )
    owner_a.refresh_from_db()
    assert owner_a.is_locked

    response = api_client.post(
        "/api/auth/login/",
        {"email": owner_a.email, "password": "StrongPassw0rd!"},
        format="json",
    )
    assert response.status_code == 423


def test_me_endpoint_requires_authentication(api_client):
    response = api_client.get("/api/auth/me/")
    assert response.status_code == 401


def test_me_endpoint_returns_current_user(api_client, owner_a):
    authenticate(api_client, owner_a)
    response = api_client.get("/api/auth/me/")
    assert response.status_code == 200
    assert response.data["email"] == owner_a.email
