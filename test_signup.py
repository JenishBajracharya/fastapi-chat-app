import requests

url = "http://127.0.0.1:8000/signup"
payload = {
    "username": "ram",
    "password": "password",
    "role": "admin"
}
response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
