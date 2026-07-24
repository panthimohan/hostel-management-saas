import pytest

from tests.conftest import authenticate

pytestmark = pytest.mark.django_db


def test_create_expense_with_named_category(api_client, owner_a, hostel_a):
    authenticate(api_client, owner_a)
    response = api_client.post(
        "/api/expenses/",
        {
            "hostel": hostel_a.id,
            "category": "ELECTRICITY",
            "title": "March electricity bill",
            "amount": "120.50",
            "payment_method": "BANK_TRANSFER",
            "incurred_on": "2026-03-01",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["category_display"] == "Electricity"


def test_miscellaneous_expense_requires_a_note(api_client, owner_a, hostel_a):
    authenticate(api_client, owner_a)
    response = api_client.post(
        "/api/expenses/",
        {
            "hostel": hostel_a.id,
            "category": "MISCELLANEOUS",
            "title": "Odd one-off cost",
            "amount": "35.00",
            "incurred_on": "2026-03-05",
        },
        format="json",
    )
    assert response.status_code == 400
    assert "note" in response.data


def test_miscellaneous_expense_succeeds_with_note(api_client, owner_a, hostel_a):
    authenticate(api_client, owner_a)
    response = api_client.post(
        "/api/expenses/",
        {
            "hostel": hostel_a.id,
            "category": "MISCELLANEOUS",
            "title": "Odd one-off cost",
            "note": "Local council inspection fee, one-time",
            "amount": "35.00",
            "incurred_on": "2026-03-05",
        },
        format="json",
    )
    assert response.status_code == 201


def test_owner_cannot_see_other_orgs_expenses(api_client, owner_a, owner_b, hostel_a, hostel_b):
    authenticate(api_client, owner_b)
    api_client.post(
        "/api/expenses/",
        {
            "hostel": hostel_b.id,
            "category": "WATER",
            "title": "Water bill",
            "amount": "40.00",
            "incurred_on": "2026-03-01",
        },
        format="json",
    )

    authenticate(api_client, owner_a)
    response = api_client.get("/api/expenses/")
    assert response.status_code == 200
    titles = [e["title"] for e in response.data["results"]]
    assert "Water bill" not in titles


def test_expense_summary_groups_by_category(api_client, owner_a, hostel_a):
    authenticate(api_client, owner_a)
    for category, amount in [("ELECTRICITY", "100.00"), ("ELECTRICITY", "50.00"), ("WATER", "30.00")]:
        api_client.post(
            "/api/expenses/",
            {
                "hostel": hostel_a.id,
                "category": category,
                "title": f"{category} bill",
                "amount": amount,
                "incurred_on": "2026-03-01",
            },
            format="json",
        )

    response = api_client.get("/api/expenses/summary/")
    assert response.status_code == 200
    assert float(response.data["total"]) == 180.00
    electricity_row = next(r for r in response.data["by_category"] if r["category"] == "ELECTRICITY")
    assert float(electricity_row["total"]) == 150.00
