import pytest
from utils_lib.api_client import APIClient

# Base URL for ReqRes public API
BASE_URL = "https://reqres.in/api"
API_KEY = "reqres-free-v1"
@pytest.fixture(scope="session")
def api_client():
    """
    Pytest fixture that initializes APIClient.
    Scope = session (reused for all tests in a session).
    """
    return APIClient(base_url=BASE_URL, api_key=API_KEY)
