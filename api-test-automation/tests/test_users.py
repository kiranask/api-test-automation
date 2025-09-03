import pytest
import json
from utils_lib.schema_validator import validate_response_schema


def test_get_single_user(api_client):
    """
    Functional + Contract test
    Step 1: Fetch user details
    Step 2: Validate status code, response schema, and business logic
    """
    resp = api_client.get("/users/2")
    assert resp.status_code == 200
    data = resp.json()

    # Validate contract
    schema = json.load(open("/Users/kkatte/PycharmProjects/rest-api-automation/api-test-automation/schemas/user_schema.json"))
    validate_response_schema(data, schema)

    # Validate content
    assert data["data"]["id"] == 2
    assert "email" in data["data"]


def test_create_user(api_client):
    """
    Functional test for user creation.
    """
    payload = {"name": "Kiran", "job": "Staff Engineer"}
    resp = api_client.post("/users", json=payload)

    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Kiran"
    assert body["job"] == "Staff Engineer"
    assert "id" in body  # Auto-generated field


@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_get_multiple_users(api_client, user_id):
    """
    Data-driven test using parameterization.
    Validates multiple users in one go.
    """
    resp = api_client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["id"] == user_id


def test_delete_user(api_client):
    """
    Negative test: Delete user
    ReqRes API returns 204 No Content for delete.
    """
    resp = api_client.delete("/users/2")
    assert resp.status_code == 204
