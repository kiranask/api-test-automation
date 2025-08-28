import requests

BASE_URL = "https://reqres.in/api"
response = requests.get(f"{BASE_URL}/users?page=2")
print(response.json())
def test_get_users():
    # Send GET request
    response = requests.get(f"{BASE_URL}/users?page=2")
    print(response)
    # Basic assertions
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

    # Check first user has required fields
    first_user = data["data"][0]
    assert "id" in first_user
    assert "email" in first_user
    assert "first_name" in first_user
    assert "last_name" in first_user
