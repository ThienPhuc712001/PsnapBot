#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test AgentRouterAnywhere Configuration
This test helps diagnose AgentRouterAnywhere setup issues
"""

import requests
import json

def test_agentrouter_anywhere():
    """Test AgentRouterAnywhere configuration"""
    print("Testing AgentRouterAnywhere Configuration...")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:6969/v1"
    
    # Test 1: Check if server is running
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/models", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running")
            models = response.json()
            print(f"   Available models: {json.dumps(models, indent=2)}")
        else:
            print(f"   ❌ Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to AgentRouterAnywhere")
        print("   Make sure AgentRouterAnywhere is running on port 6969")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Test chat completion without Authorization header
    print("\n2. Testing chat completion (no auth)...")
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, please respond with 'API working'"}
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"   ✅ Success: {content}")
            return True
        else:
            print(f"   ❌ Error Response: {response.text}")
            
            # Analyze common errors
            if response.status_code == 403:
                print("\n   403 Forbidden - Possible causes:")
                print("   - Model 'glm-4.6' not configured in AgentRouterAnywhere")
                print("   - Provider API key missing or invalid")
                print("   - Provider not properly configured")
            elif response.status_code == 404:
                print("\n   404 Not Found - Possible causes:")
                print("   - Endpoint path incorrect")
                print("   - AgentRouterAnywhere version incompatible")
            elif response.status_code == 500:
                print("\n   500 Internal Server Error - Possible causes:")
                print("   - Provider API error")
                print("   - Model not available")
                
            return False
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return False

def show_configuration_guide():
    """Show AgentRouterAnywhere configuration guide"""
    print("\n" + "=" * 50)
    print("AgentRouterAnywhere Configuration Guide")
    print("=" * 50)
    
    print("\nTo fix the 403 error, check your AgentRouterAnywhere setup:")
    print("\n1. Open AgentRouterAnywhere application")
    print("2. Go to Settings")
    print("3. Click 'Add Provider'")
    print("4. Select 'OpenAI' as provider type")
    print("5. Fill in the following:")
    print("   - Provider Name: GLM-4.6 (or any name)")
    print("   - API URL: https://open.bigmodel.cn/api/paas/v4/")
    print("   - API Key: YOUR_ZHIPU_API_KEY")
    print("   - Model Name: glm-4.6")
    print("6. Click 'Save'")
    print("7. Make sure the provider is enabled")
    print("\nNote: You need a valid Zhipu AI API key for GLM-4.6")
    print("Get one from: https://open.bigmodel.cn/")

def main():
    """Run the test"""
    success = test_agentrouter_anywhere()
    
    if not success:
        show_configuration_guide()
        return 1
    else:
        print("\n✅ AgentRouterAnywhere is configured correctly!")
        print("PSnapBOT should work now.")
        return 0

if __name__ == "__main__":
    exit(main())