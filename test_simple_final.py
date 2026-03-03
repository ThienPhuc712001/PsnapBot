#!/usr/bin/env python3
"""
Simple final test for PSnapBOT
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config_user import get_api_config
    print("SUCCESS: Imported config_user")
    
    config = get_api_config()
    print(f"API Key: {config['api_key'][:10]}...")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {config['model']}")
    
    # Test direct API call
    import requests
    import json
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": config['model'],
        "messages": [
            {"role": "user", "content": "Hello, say 'API connection successful'"}
        ],
        "max_tokens": 50
    }
    
    print("\nTesting API connection...")
    response = requests.post(
        f"{config['base_url']}/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        content = result['choices'][0]['message']['content']
        print(f"API Response: {content}")
        print("\nSUCCESS: PSnapBOT API connection is working!")
    else:
        print(f"ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed.")