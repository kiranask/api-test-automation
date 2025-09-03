import pytest

def test_successful_login(api_client):
    """
    Positive authentication test.
    """
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    resp = api_client.post("/login", json=payload)
    assert resp.status_code == 200
    assert "token" in resp.json()

def test_unsuccessful_login(api_client):
    """
    Negative authentication test: Missing password.
    """
    payload = {"email": "peter@klaven"}
    resp = api_client.post("/login", json=payload)
    assert resp.status_code == 400
    assert resp.json()["error"] == "Missing password"
