# conftest.py
# This file is a special Pytest configuration file.
# Pytest will automatically discover it and load any fixtures defined here.
# Fixtures are reusable "setup" functions that provide data or objects for tests.

import pytest
from src.api_client import APIClient  # Importing our custom API client class


# Fixture 1: Base URL
@pytest.fixture(scope="session")
def base_url():
    """
    Fixture that provides the base URL of the API.
    - scope="session" means this fixture is created once per test run (shared across all tests).
    - Useful for constants that do not change often.
    """
    return "https://reqres.in/api"


# Fixture 2: API Client
@pytest.fixture
def client(base_url):
    """
    Fixture that creates and returns an instance of APIClient.
    - Depends on the 'base_url' fixture.
    - This provides a ready-to-use client object for making API calls in tests.
    """
    return APIClient(base_url)
