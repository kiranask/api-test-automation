# src/api_client.py
# ----------------------------------------------------------------------------
# Why: Central API client wrapper so that all tests use consistent request
#      logic (base_url, headers, timeouts) instead of duplicating code.
# What: A thin abstraction layer around the 'requests' library.
# How:  Tests call client.get("/path") or client.post("/path") instead of
#       raw requests.get(). This makes tests cleaner, maintainable, and DRY.
# ----------------------------------------------------------------------------

import json
import requests

class APIClient:
    """
    APIClient provides helper methods for GET/POST requests with a base_url.
    Uses requests.Session() for connection reuse (faster than plain requests).
    """

    def __init__(self, base_url: str, timeout: int = 10):
        # Store the base URL (e.g., https://reqres.in/api)
        # Remove any trailing slashes / at the end of the string.
        # "https://reqres.in/api/".rstrip("/")  # → "https://reqres.in/api"
        self.base_url = base_url.rstrip('/')

        # Use a session to persist headers and reuse TCP connections
        self.session = requests.Session()
        # Default: ask server to return JSON
        self.session.headers.update({"Accept": "application/json"})
        # Set a default timeout for all requests
        self.timeout = timeout

    def url(self, path: str) -> str:
        """
        Build full URL from base_url + relative path.
        Example: client._url('/users') -> https://reqres.in/api/users
        """
        if path.startswith("http"):
            return path
        # lstrip('/') removes leading slashes / at the beginning of a string.
        # "/users".lstrip("/")   # → "users"
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: dict = None, headers: dict = None) -> requests.Response:
        """Send GET request."""
        return self.session.get(self.url(path), params=params, headers=headers, timeout=self.timeout)

    def post(self, path: str, json_payload: dict = None, data: dict = None, headers: dict = None) -> requests.Response:
        """Send POST request with JSON or form data."""
        return self.session.post(self.url(path), json=json_payload, data=data, headers=headers, timeout=self.timeout)

    @staticmethod
    def is_json_response(resp: requests.Response) -> bool:
        """
        Check if response Content-Type is JSON (application/json, vendor+json, etc.)
        """
        ct = resp.headers.get("Content-Type", "").lower()
        return ("application/json" in ct) or (ct.endswith("+json")) or ("json" in ct)

    @staticmethod
    def json_or_text(resp: requests.Response):
        """
        Try to parse JSON safely.
        If not valid JSON, return raw text (helps in debugging error responses).
        """
        try:
            return resp.json()
        except (ValueError, json.JSONDecodeError):
            return resp.text
