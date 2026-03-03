#!/usr/bin/env python3
"""
Test AgentRouterAnywhere local endpoint
"""
import requests
import json

def test_local_endpoint():
    """Test local AgentRouterAnywhere endpoint"""
    
    # Test without API key first
    print("Testing local endpoint without API key...")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, say 'Local endpoint working'"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:6969/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"SUCCESS: {content}")
            return True
        else:
            print("FAILED: Endpoint not working without API key")
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Test with API key
    print("\nTesting with API key...")
    headers["Authorization"] = "Bearer sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"
    
    try:
        response = requests.post(
            "http://127.0.0.1:6969/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"SUCCESS: {content}")
            return True
        else:
            print("FAILED: Endpoint not working with API key")
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=== AgentRouterAnywhere Local Endpoint Test ===")
    test_local_endpoint()
    print("\nTest completed.")