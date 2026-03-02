#!/usr/bin/env python3
"""
Simple test script for PSnapBOT API connection
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config_agentrouter import get_agentrouter_config, print_config_status
    print("✓ Successfully imported config_agentrouter")
    
    print("\n=== AgentRouter Configuration Status ===")
    print_config_status()
    
    config = get_agentrouter_config()
    print(f"\n✓ API Key configured: {'Yes' if config['api_key'] else 'No'}")
    print(f"✓ Base URL: {config['base_url']}")
    print(f"✓ Model: {config['model']}")
    
    print("\n=== Testing API Connection ===")
    
    import requests
    import json
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
        "User-Agent": "PSnapBOT/1.0"
    }
    
    # Test simple completion
    data = {
        "model": config['model'],
        "messages": [
            {"role": "user", "content": "Hello, can you respond with just 'API working'?"}
        ],
        "max_tokens": 10,
        "temperature": 0.1
    }
    
    print(f"Sending request to: {config['base_url']}/chat/completions")
    
    response = requests.post(
        f"{config['base_url']}/chat/completions",
        headers=headers,
        json=data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(f"✓ API Response: {content}")
            print("\n✓ PSnapBOT API connection test PASSED!")
        else:
            print("✗ Unexpected response format")
            print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print(f"✗ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
    
print("\n=== Test Complete ===")