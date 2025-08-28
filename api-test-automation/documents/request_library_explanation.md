#  Python Requests Library - Step by Step Guide

This document will help you explain how the `requests` library works in Python, with clear examples you can use in your API automation classes.

---

## 🔹 1. What is `requests`?

* `requests` is a popular Python library used to send **HTTP/HTTPS requests**.
* It allows us to interact with **REST APIs** easily (GET, POST, PUT, DELETE).
* Example:

  ```python
  import requests

  response = requests.get("https://reqres.in/api/users?page=2")
  print(response.status_code)  # 200
  print(response.json())       # JSON response from API
  ```

---

## 🔹 2. Why use it in API Automation?

* Easy to send requests and handle responses.
* Supports query parameters, headers, authentication, sessions.
* Works well with **pytest** for automation.

---

## 🔹 3. What is `requests.Session()`?

* A **session** object helps:

  * Reuse the same TCP connection → faster tests.
  * Store **common headers, cookies, and authentication** across requests.

Example:

```python
session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

response = session.get("https://reqres.in/api/users?page=2")
print(response.json())
```

⚡ Benefit: You don’t need to pass headers again and again.

---

## 🔹 4. Handling Expired Sessions

* Some APIs have session expiry (like login sessions).
* If expired → server returns `401 Unauthorized` or `403 Forbidden`.
* Solution: re-authenticate and refresh session before retrying request.

---

## 🔹 5. Example: API Client Class

We usually wrap `requests` in a reusable **API client class**.

```python
import requests

class APIClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: dict = None, headers: dict = None) -> requests.Response:
        """Send GET request."""
        return self.session.get(
            self.url(path),
            params=params,
            headers=headers,
            timeout=self.timeout
        )

    def post(self, path: str, json: dict = None, headers: dict = None) -> requests.Response:
        """Send POST request."""
        return self.session.post(
            self.url(path),
            json=json,
            headers=headers,
            timeout=self.timeout
        )
```

---

## 🔹 6. Why These Arguments?

### In `get()` method:

* **`path: str`** → relative API endpoint (e.g., `users`).
* **`params: dict`** → query parameters (`?page=2`).
* **`headers: dict`** → request-specific headers.
* **`timeout=self.timeout`** → ensures test doesn’t hang forever.

### Example:

```python
client = APIClient("https://reqres.in/api")
response = client.get("users", params={"page": 2})
print(response.url)  # https://reqres.in/api/users?page=2
```

### In `post()` method:

* **`json: dict`** → body data in JSON format.
* **`headers: dict`** → request-specific headers.

Example:

```python
response = client.post("users", json={"name": "morpheus", "job": "leader"})
print(response.json())
```

---

## 🔹 7. How to Know Response is JSON?

* Check `Content-Type` header:

```python
print(response.headers["Content-Type"])  # application/json
```

* If `application/json`, then `response.json()` can be used safely.

---

## 🔹 8. Supporting Files in Framework

### `pytest.ini`

* Configures pytest behavior (test discovery, markers, logging).
* Example:

  ```ini
  [pytest]
  markers =
      smoke: Quick tests for critical APIs
      regression: Full suite tests
  addopts = -v --maxfail=1 --disable-warnings
  ```

### `requirements.txt`

* Lists project dependencies.
* Example:

  ```
  requests
  pytest
  pytest-html
  ```

Command to install:

```bash
pip install -r requirements.txt
```

---

# ✅ Summary for Teaching

1. Explain `requests` basics with GET.
2. Show sessions and why they are faster.
3. Show reusable `APIClient` class.
4. Explain arguments (`params`, `headers`, `timeout`, `json`).
5. Show how to check `Content-Type`.
6. Explain supporting files (`pytest.ini`, `requirements.txt`).
