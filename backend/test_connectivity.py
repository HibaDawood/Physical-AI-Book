import requests
import json

def test_backend_connectivity():
    """Test the backend API connectivity"""
    print("Testing backend connectivity...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        print("Make sure the backend server is running on http://localhost:8000")
        return False
    
    # Test chat endpoint
    try:
        test_payload = {
            "message": "What is Physical AI?",
            "history": []
        }
        
        response = requests.post(
            "http://localhost:8000/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_payload)
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Chat endpoint test: SUCCESS")
            print(f"Response keys: {list(result.keys())}")
            print(f"Response text (first 100 chars): {result.get('response', '')[:100]}...")
        else:
            print(f"Chat endpoint test: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Chat endpoint test: FAILED - {e}")
        return False
    
    # Test query endpoint
    try:
        test_payload = {
            "query": "What is Physical AI?"
        }
        
        response = requests.post(
            "http://localhost:8000/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_payload)
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Query endpoint test: SUCCESS")
            print(f"Response keys: {list(result.keys())}")
            print(f"Answer text (first 100 chars): {result.get('answer', '')[:100]}...")
        else:
            print(f"Query endpoint test: FAILED - Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Query endpoint test: FAILED - {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_backend_connectivity()
    if success:
        print("\n✓ All backend tests passed!")
    else:
        print("\n✗ Backend tests failed. Please check the server configuration.")