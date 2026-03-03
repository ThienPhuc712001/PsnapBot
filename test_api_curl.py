#!/usr/bin/env python3
"""
Test API with different methods
"""
import requests
import json
import subprocess
import sys

def test_with_curl():
    """Test with curl command"""
    
    print("=== Testing with curl ===")
    
    # Test local endpoint
    curl_command = [
        'curl', '-X', 'POST',
        'http://127.0.0.1:6969/v1/chat/completions',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Bearer sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g',
        '-d', json.dumps({
            "model": "glm-4.6",
            "messages": [
                {"role": "user", "content": "Hello, say 'API working'"}
            ],
            "max_tokens": 50
        })
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=30)
        print(f"Exit code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            print("SUCCESS: curl request completed")
        else:
            print("FAILED: curl request failed")
            
    except Exception as e:
        print(f"ERROR: {e}")

def test_with_python_direct():
    """Test with Python requests directly"""
    
    print("\n=== Testing with Python requests ===")
    
    # Test local endpoint
    url = "http://127.0.0.1:6969/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"
    }
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, say 'Python working'"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"SUCCESS: {content}")
        else:
            print(f"FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR: {e}")

def test_cloud_endpoint():
    """Test cloud endpoint"""
    
    print("\n=== Testing Cloud Endpoint ===")
    
    url = "http://127.0.0.1:6969/v1"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"
    }
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, say 'Cloud working'"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"SUCCESS: {content}")
        else:
            print(f"FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    print("=== Comprehensive API Test ===")
    
    # Test different methods
    test_with_curl()
    test_with_python_direct()
    test_cloud_endpoint()
    
    print("\n=== Test Summary ===")
    print("If all tests fail with 401/403 errors:")
    print("1. Check if API key is valid")
    print("2. Verify Discord account is properly verified")
    print("3. Check if AgentRouterAnywhere needs provider configuration")
    print("4. Try getting a new API key from Discord")
    
    print("\nTest completed.")