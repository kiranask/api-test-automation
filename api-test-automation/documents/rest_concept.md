REST API Concepts
1. What is an API?

API (Application Programming Interface) is a way for two applications to talk to each other.

Example: Your weather app calls a weather API to get today’s temperature.

2. What is REST API?

REST (Representational State Transfer) is a style of API that uses HTTP for communication.

It follows these principles:

Stateless → Each request is independent (server doesn’t remember previous requests).

Client-Server → Client (your code) and Server (API provider) are separate.

Uniform Interface → Resources are represented via URLs (endpoints).

Resource Manipulation via HTTP Methods.

3. HTTP Methods (CRUD Operations)
HTTP Method	CRUD Operation	Example Use Case
GET	Read	Get list of users
POST	Create	Add a new user
PUT	Update (replace)	Replace user data
PATCH	Update (partial)	Update user’s email only
DELETE	Delete	Remove a user
4. API Endpoints

An endpoint is a specific URL where an API can be accessed.

Example using reqres.in
:

https://reqres.in/api/users → endpoint for managing users

https://reqres.in/api/users/2 → endpoint for a specific user

5. Requests & Responses

When your Python code makes a request, two key things happen:

Request → Client sends data to the server

URL (endpoint)

Method (GET, POST, etc.)

Headers (extra info like Content-Type)

Body (data in JSON or form format for POST/PUT)

Response → Server sends back

Status Code (200 OK, 201 Created, 404 Not Found, 500 Error)

Headers (info about response)

Body (data in JSON, XML, HTML, etc.)

6. JSON vs Data in Requests

json parameter → Used when API expects JSON body.

response = requests.post("https://reqres.in/api/users", 
                         json={"name": "John", "job": "Engineer"})


Sent as:

{
  "name": "John",
  "job": "Engineer"
}


data parameter → Used for form-encoded data (like HTML forms).

response = requests.post("https://reqres.in/api/users", 
                         data={"username": "john", "password": "1234"})


Sent as:

username=john&password=1234

7. Why Write an API Client?

Reusability → Instead of writing requests.get() everywhere, you wrap it in a class.

Consistency → Common logic (base URL, timeout, headers) is centralized.

Maintainability → If something changes (like auth headers), you update in one place.

Example API Client:

import requests

class APIClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: dict = None, headers: dict = None):
        return self.session.get(self.url(path), params=params, headers=headers, timeout=self.timeout)

    def post(self, path: str, json_payload: dict = None, data: dict = None, headers: dict = None):
        return self.session.post(self.url(path), json=json_payload, data=data, headers=headers, timeout=self.timeout)

8. Example Usage
client = APIClient("https://reqres.in/api")

# GET users
response = client.get("users?page=2")
print(response.json())

# POST new user (JSON body)
response = client.post("users", json_payload={"name": "John", "job": "Engineer"})
print(response.json())
