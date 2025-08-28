#1 — What is REST (quick)

REST = REpresentational State Transfer — an architectural style for networked applications.

Main idea: model server functionality as resources (nouns) accessed via URLs (endpoints) and manipulated with HTTP verbs (GET/POST/PUT/DELETE).

Key constraints: client-server, stateless, cacheable, uniform interface, layered system (code-on-demand optional).

#2 — Core terms (must-know)

Resource: anything the API exposes (users, orders).

Endpoint / URI: the URL where you access a resource, e.g. https://api.example.com/v1/users/2.

Representation: the data format returned (JSON, XML).

HTTP method:

GET → read (safe, idempotent)

POST → create (not idempotent)

PUT → replace/update (idempotent)

PATCH → partial update (not necessarily idempotent)

DELETE → remove (idempotent usually)

Headers: metadata (Content-Type, Accept, Authorization).

Query params: ?page=2&limit=10 (filters, pagination).

Path params: /users/2 (resource identifier).

3 — Anatomy of a request (what requests sends)
GET /users?page=2 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer <token>


method, url (scheme + host + path), headers, params (querystring), body (for POST/PUT/PATCH).

4 — Anatomy of a response (what requests receives)

Status code (200, 201, 400, 401, 404, 500...) — tells success/failure cause.

Headers — e.g., Content-Type: application/json; charset=utf-8.

Body — actual payload (JSON most common).

Common status codes to teach:

200 OK, 201 Created, 204 No Content

400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found

409 Conflict (duplicate), 429 Too Many Requests (rate limit)

5xx server errors

5 — Content types & body formats

application/json → JSON body (resp.json() in requests).

application/x-www-form-urlencoded → form data (requests.post(..., data=payload)).

multipart/form-data → file uploads.

Always check Content-Type header before parsing:

ct = resp.headers.get("Content-Type","").lower()
if "application/json" in ct: data = resp.json()
else: data = resp.text

6 — REST design best practices (how to design endpoints)

Use nouns (resources), plural: /users, /orders.

Keep hierarchy: /users/{user_id}/orders.

Use query params for filtering/pagination: /users?role=admin&page=2.

Version your API: /v1/users (API evolution).

Use appropriate status codes.

Avoid verbs in URL (bad: /getUserById).

Provide consistent error format:

{ "error": { "code": 404, "message": "User not found", "details": null } }

7 — Idempotency and safety (teach this clearly)

Safe = does not modify server (GET, HEAD).

Idempotent = same request repeated yields same result/state (PUT, DELETE, GET).

POST is normally not idempotent (submitting twice creates two resources).

8 — Authentication & security (overview)

Always use HTTPS.

Common auth patterns:

API keys (header/query)

Bearer tokens / JWT (Authorization: Bearer <token>)

OAuth2 flows (authorization, refresh tokens)

Session cookies (login → cookie stored in Session)

Handle token expiry: detect 401 → refresh token or re-login.

9 — Why an APIClient wrapper? (class explanation)

Centralizes base_url, headers, timeouts, auth, retry logic.

Avoids repeated boilerplate in tests.

Makes tests readable: client.get("/users/2") is clearer than building full URL + headers + timeout each time.

10 — Practical requests examples (copy & demo)

GET with query params

import requests
resp = requests.get("https://reqres.in/api/users", params={"page": 2}, timeout=5)
print(resp.status_code, resp.url)
if "application/json" in resp.headers.get("Content-Type","").lower():
    print(resp.json())


POST JSON

resp = requests.post("https://reqres.in/api/users", json={"name":"Kiran","job":"DevOps"}, timeout=5)
print(resp.status_code, resp.json())


POST form-data (data) vs JSON (json)

# form encoded
resp = requests.post("https://httpbin.org/post", data={"k":"v"})
# json encoded
resp = requests.post("https://httpbin.org/post", json={"k":"v"})


Session usage (connection reuse + auth)

s = requests.Session()
s.headers.update({"Accept":"application/json"})
# login once
login = s.post("https://api.example.com/v1/login", json={"user":"a","pwd":"b"})
token = login.json().get("access_token")
s.headers.update({"Authorization": f"Bearer {token}"})
# subsequent requests reuse connection and token
resp = s.get("https://api.example.com/v1/users")


Robust parse helper

def json_or_text(resp):
    try:
        return resp.json()
    except ValueError:
        return resp.text

11 — Handling expired auth (retry pattern)

Short pattern to teach:

def request_with_reauth(session, method, url, login_fn, retries=1, **kwargs):
    resp = session.request(method, url, **kwargs)
    if resp.status_code == 401 and retries:
        login_fn()  # perform login and update session headers
        return request_with_reauth(session, method, url, login_fn, retries-1, **kwargs)
    return resp

12 — Error handling & testing tips

Check status_code first; assert expected codes in tests.

Check Content-Type before json().

Timeouts are essential in automation: timeout=5.

Use session for repeated calls.

For flaky APIs, add limited retries with backoff (don’t mask genuine bugs).

13 — Demonstration-ready APIClient snippet (compact)
import requests

class APIClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept":"application/json"})

    def _url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path, params=None, headers=None):
        return self.session.get(self._url(path), params=params, headers=headers, timeout=self.timeout)

    def post(self, path, json_payload=None, data=None, headers=None):
        return self.session.post(self._url(path), json=json_payload, data=data, headers=headers, timeout=self.timeout)

    @staticmethod
    def is_json_response(resp):
        ct = resp.headers.get("Content-Type","").lower()
        return "application/json" in ct or ct.endswith("+json")

14 — Classroom plan (1-hour lesson focused on REST basics)

0–5 min: Learning goals + quick REST definition
5–20 min: HTTP methods + resource vs endpoint (live URL examples)
20–35 min: Request/response anatomy + headers + Content-Type demo with requests
35–50 min: Live demo: write a small test with APIClient (GET and POST) and show response.json() vs .text
50–60 min: Q&A + quick exercise (students implement GET with params and assert page value)

15 — Quick exercises for students

GET /users?page=2 — assert status_code==200 and response contains page==2.

POST /users with json={"name":"x","job":"y"} — assert 201 and id in response.

Simulate expired token: call a protected endpoint then handle 401 with re-login stub.

16 — Common interview/class questions & short answers

Q: Why use json= vs data=?
A: json= sends application/json body (JSON). data= sends form-encoded data.

Q: When to use PUT vs PATCH?
A: PUT replaces full resource (idempotent); PATCH changes part (partial).

Q: What is idempotent?
A: Repeating the same request has the same effect as doing it once (no additional side-effects).

Q: How to detect JSON?
A: Check Content-Type header for application/json then call resp.json().

17 — Cheat sheet (one-liners)

Build url: f"{base.rstrip('/')}/{path.lstrip('/')}"

Check JSON: if "application/json" in resp.headers.get("Content-Type","").lower(): resp.json()

GET with params: requests.get(url, params={"page":2})

POST json: requests.post(url, json={"k":"v"})

Post form: requests.post(url, data={"k":"v"})

Session: s = requests.Session(); s.headers.update({...})