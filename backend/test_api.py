import requests
import json

def test_api():
    """Simple test to verify the API is working"""
    print("Testing the RAG API...")
    
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print("✓ Health check passed")
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Health check failed with error: {e}")
        print("Make sure the backend API is running on http://127.0.0.1:8000")
        return
    
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
            print("✓ Query test passed")
            print(f"Sample response: {result['answer'][:100]}...")
        else:
            print(f"✗ Query test failed with status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Query test failed with error: {e}")
        print("Make sure the backend API is running on http://127.0.0.1:8000")

if __name__ == "__main__":
    test_api()