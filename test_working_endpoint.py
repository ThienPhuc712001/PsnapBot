#!/usr/bin/env python3
"""
Test the working endpoint in detail
"""
import sys
import os
import requests
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

API_KEY = "sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"

def test_working_endpoint():
    """Test the endpoint that returned 200"""
    
    endpoint = "https://agentrouter.org/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4.6",
        "messages": [
            {"role": "user", "content": "Hello, respond with 'Working'"}
        ],
        "max_tokens": 10
    }
    
    print(f"Testing endpoint: {endpoint}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response Text: {repr(response.text)}")
        print(f"Response Content: {response.content}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"JSON Response: {json.dumps(result, indent=2)}")
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"\n[SUCCESS] API Response: {content}")
                    return True
                else:
                    print("[WARNING] Unexpected JSON structure")
                    
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON decode error: {e}")
                print("Response is not valid JSON")
                
        else:
            print(f"[ERROR] HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
    
    return False

if __name__ == "__main__":
    success = test_working_endpoint()
    
    if success:
        print("\n[SUCCESS] Found working API configuration!")
        print("Updating configuration...")
        
        # Update the config file with working endpoint
        try:
            with open('config_agentrouter.py', 'r') as f:
                content = f.read()
            
            # Replace the base_url
            new_content = content.replace(
                "base_url = 'https://agentrouter.org/v1'",
                "base_url = 'https://agentrouter.org'"
            )
            
            with open('config_agentrouter.py', 'w') as f:
                f.write(new_content)
                
            print("[OK] Updated config_agentrouter.py with working endpoint")
            
        except Exception as e:
            print(f"[ERROR] Failed to update config: {e}")
    else:
        print("\n[ERROR] Could not establish working connection")