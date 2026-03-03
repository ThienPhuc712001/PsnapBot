#!/usr/bin/env python3
"""
Test AgentRouterAnywhere without authentication
"""
import requests
import json

def test_no_auth():
    """Test without Authorization header"""
    
    print("Testing without Authorization header...")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, say 'Working without auth'"}
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
            print("FAILED: Still getting error")
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_with_empty_auth():
    """Test with empty Authorization header"""
    
    print("\nTesting with empty Authorization header...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "
    }
    
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, say 'Working with empty auth'"}
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
            print("FAILED: Still getting error")
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=== AgentRouterAnywhere Authentication Test ===")
    
    success1 = test_no_auth()
    success2 = test_with_empty_auth()
    
    if success1 or success2:
        print("\nSUCCESS: Found working authentication method")
    else:
        print("\nFAILED: Need to configure AgentRouterAnywhere provider")
        print("Please add a provider in AgentRouterAnywhere settings")
    
    print("\nTest completed.")