#!/usr/bin/env python3
"""
Debug request to see exact headers and payload
"""
import sys
import os
import requests
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_agentrouter import get_agentrouter_config, get_headers

try:
    config = get_agentrouter_config()
    headers = get_headers()
    
    print("=== DEBUG REQUEST INFO ===")
    print(f"API Key: {config['api_key'][:20]}...{config['api_key'][-10:]}")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {config['model']}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    payload = {
        "model": config['model'],
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 10
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    url = f"{config['base_url']}/chat/completions"
    print(f"Full URL: {url}")
    
    print("\n=== SENDING REQUEST ===")
    
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"JSON Response: {json.dumps(result, indent=2)}")
    else:
        print(f"Error Details: {response.status_code} - {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()

print("\nDebug completed.")