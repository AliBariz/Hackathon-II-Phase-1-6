"""
Debug script to test the chat endpoint functionality with a real user
"""
import requests
import json

def test_chat_endpoint():
    # Get a real user from the database first
    # Since I can't directly query the database from here, I'll use a known user ID from the system
    # Based on the error logs earlier, we know there's a user with ID: fcd35ff4-db7d-4d6c-83b6-c27519693995

    user_id = "fcd35ff4-db7d-4d6c-83b6-c27519693995"  # This is from the original error
    url = f"http://localhost:8000/api/{user_id}/chat"

    # Test payload to add a task
    payload = {
        "user_id": user_id,
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }

    print(f"Testing chat endpoint with user ID: {user_id}")
    print(f"Payload: {payload}")

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Chat endpoint is working!")
            # Parse the response
            response_json = response.json()
            print(f"Bot Response: {response_json.get('response', 'N/A')}")
        else:
            print("ERROR: Chat endpoint is still failing!")

    except Exception as e:
        print(f"ERROR connecting to server: {str(e)}")
        print("Make sure the backend server is running on port 8000")

def test_with_generic_user():
    """Test with a generic user ID that might exist"""
    user_id = "test_user_123"
    url = f"http://localhost:8000/api/{user_id}/chat"

    # Test payload to add a task
    payload = {
        "user_id": user_id,
        "message": "Add a task to test the system",
        "conversation_id": None
    }

    print(f"\nTesting chat endpoint with generic user ID: {user_id}")
    print(f"Payload: {payload}")

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Chat endpoint is working!")
            # Parse the response
            response_json = response.json()
            print(f"Bot Response: {response_json.get('response', 'N/A')}")
        else:
            print("ERROR: Chat endpoint is still failing!")

    except Exception as e:
        print(f"ERROR connecting to server: {str(e)}")

if __name__ == "__main__":
    test_chat_endpoint()
    test_with_generic_user()