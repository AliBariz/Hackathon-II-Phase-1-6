import requests
import json

# Test the backend auth endpoints
BASE_URL = "http://localhost:8000"

print("Testing backend connectivity...")

try:
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

    # Test auth endpoints
    response = requests.options(f"{BASE_URL}/auth/login")
    print(f"OPTIONS /auth/login: {response.status_code}")
    print(f"CORS headers: {dict(response.headers)}")

    response = requests.options(f"{BASE_URL}/auth/register")
    print(f"OPTIONS /auth/register: {response.status_code}")
    print(f"CORS headers: {dict(response.headers)}")

except Exception as e:
    print(f"Error testing backend: {e}")