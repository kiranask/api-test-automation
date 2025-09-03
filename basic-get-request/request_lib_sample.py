""" What is there in the response"""
import requests

response = requests.get("https://reqres.in/api/users/2")
print(response.status_code)
"""
If Content-Type contains application/json, it means the body is JSON.
Other common values you might see:

text/html → normal webpage

application/xml → XML

text/plain → plain text
"""
if "application/json" in response.headers["Content-Type"]:

    response = response.json()


print(response["data"])
