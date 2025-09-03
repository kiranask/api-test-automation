import requests
import logging


class APIClient:
    """
    A reusable API client wrapper on top of 'requests'.
    Provides common methods for GET, POST, PUT, DELETE requests.
    Handles base URL and authentication headers in one place.
    """

    def __init__(self, base_url, token=None, api_key=None):
        self.base_url = base_url
        self.headers = {}
        if token:
            self.headers = {"Authorization": f"Bearer {token}"}
        if api_key:
            self.headers["x-api-key"] = api_key

    def get(self, endpoint, **kwargs):
        logging.info(f"GET {endpoint}")
        return requests.get(f"{self.base_url}{endpoint}", headers=self.headers, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        logging.info(f"POST {endpoint}")
        return requests.post(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json, **kwargs)

    def put(self, endpoint, json=None, **kwargs):
        logging.info(f"PUT {endpoint}")
        return requests.put(f"{self.base_url}{endpoint}", headers=self.headers, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        logging.info(f"DELETE {endpoint}")
        return requests.delete(f"{self.base_url}{endpoint}", headers=self.headers, **kwargs)
