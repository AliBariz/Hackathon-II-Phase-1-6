"""
Debug script to test the chat endpoint functionality
"""
import requests
import json

def test_chat_endpoint():
    # Test the chat endpoint
    url = "http://localhost:8000/api/test-user/chat"

    # Test payload to add a task
    payload = {
        "user_id": "test-user",
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Chat endpoint is working!")
        else:
            print("ERROR: Chat endpoint is still failing!")

    except Exception as e:
        print(f"ERROR connecting to server: {str(e)}")
        print("Make sure the backend server is running on port 8000")

if __name__ == "__main__":
    test_chat_endpoint()