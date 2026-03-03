#!/usr/bin/env python3
"""
Test script for AgentRouter API with different endpoints
"""
import requests
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_agentrouter import get_agentrouter_config

def test_different_endpoints():
    """Test different AgentRouter endpoints"""
    config = get_agentrouter_config()
    
    endpoints_to_test = [
        "http://127.0.0.1:6969/v1/chat/completions",
        "http://127.0.0.1:6969/api/v1/chat/completions",
        "http://127.0.0.1:6969/v1/completions",
        "http://127.0.0.1:6969/api/v1/completions"
    ]
    
    print("Testing different AgentRouter endpoints...")
    print("=" * 60)
    
    for endpoint in endpoints_to_test:
        print(f"\nTesting endpoint: {endpoint}")
        
        try:
            payload = {
                "model": config["model"],
                "messages": [
                    {
                        "role": "user", 
                        "content": "Hello, this is a test message."
                    }
                ],
                "max_tokens": 50
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                timeout=config["timeout"],
                headers=config["headers"]
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print("  SUCCESS: This endpoint works!")
                return endpoint
            else:
                print(f"  FAILED: {response.status_code}")
                print(f"  Error: {response.text[:100]}")
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")
    
    return None

def main():
    """Test different AgentRouter endpoints"""
    print("AgentRouter Endpoint Discovery Test")
    print("=" * 60)
    
    working_endpoint = test_different_endpoints()
    
    if working_endpoint:
        print(f"\n" + "=" * 60)
        print(f"WORKING ENDPOINT: {working_endpoint}")
        print("\nUpdate config_agentrouter.py with:")
        print(f'API_BASE_URL = "{working_endpoint}"')
        print("\nThen test again with:")
        print("  test_agentrouter.py")
    else:
        print("\n" + "=" * 60)
        print("No working endpoint found.")
        print("Please check AgentRouter documentation or contact support.")
    
    return 0 if working_endpoint else 1

if __name__ == "__main__":
    sys.exit(main())