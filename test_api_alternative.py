#!/usr/bin/env python3
"""
Alternative API test for AgentRouter
"""
import sys
import os
import requests
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

API_KEY = "sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"

def test_different_endpoints():
    """Test different AgentRouter endpoints"""
    
    endpoints = [
        "https://agentrouter.org/v1/chat/completions",
        "https://agentrouter.org/api/v1/chat/completions", 
        "https://api.agentrouter.org/v1/chat/completions",
        "https://agentrouter.org/chat/completions"
    ]
    
    headers_variants = [
        {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "PSnapBOT/1.0"
        },
        {
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        },
        {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
    ]
    
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 10
    }
    
    print("Testing different endpoints and headers...")
    
    for endpoint in endpoints:
        print(f"\n--- Testing endpoint: {endpoint} ---")
        
        for i, headers in enumerate(headers_variants):
            print(f"Headers variant {i+1}: {list(headers.keys())}")
            
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=data,
                    timeout=10
                )
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print("SUCCESS! Response:", result.get('choices', [{}])[0].get('message', {}).get('content', 'No content'))
                    return True
                else:
                    print(f"Error: {response.text[:200]}")
                    
            except Exception as e:
                print(f"Exception: {e}")
    
    return False

if __name__ == "__main__":
    success = test_different_endpoints()
    
    if success:
        print("\n[SUCCESS] Found working configuration!")
    else:
        print("\n[ERROR] No working configuration found.")
        print("Please check:")
        print("1. API key is valid and active")
        print("2. Account has sufficient credits")
        print("3. Correct endpoint URL")
        print("4. Model 'glm-4.6' is available")