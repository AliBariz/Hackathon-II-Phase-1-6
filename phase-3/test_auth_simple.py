import requests
import json

# Test the actual auth endpoints (not just OPTIONS)
BASE_URL = "http://localhost:8000"

print("Testing actual backend auth endpoints...")

try:
    # Test the login endpoint with a simple request
    headers = {
        'Content-Type': 'application/json',
    }

    # Try login with dummy data (expecting a 422 or 401, not a CORS error)
    response = requests.post(f"{BASE_URL}/auth/login",
                           headers=headers,
                           json={"email": "test@test.com", "password": "password"})
    print(f"POST /auth/login: {response.status_code}")
    print(f"Response: {response.text}")

    # Test the register endpoint
    response = requests.post(f"{BASE_URL}/auth/register",
                           headers=headers,
                           json={"email": "test@test.com", "password": "password123A@"})
    print(f"POST /auth/register: {response.status_code}")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"Error testing backend: {e}")