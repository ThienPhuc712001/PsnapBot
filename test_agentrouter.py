#!/usr/bin/env python3
"""
Test script for AgentRouter API connection
"""
import requests
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_agentrouter import get_agentrouter_config

def test_agentrouter_api():
    """Test AgentRouter API connection"""
    print("Testing PSnapBOT with AgentRouter API...")
    print("=" * 50)
    
    config = get_agentrouter_config()
    
    try:
        # Test API with a simple request
        payload = {
            "model": config["model"],
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello, this is a test message. Please respond with 'AgentRouter connection successful!'"
                }
            ],
            "max_tokens": 50
        }
        
        print(f"Connecting to: {config['base_url']}")
        print(f"Using model: {config['model']}")
        print(f"Using headers: {config['headers']}")
        
        response = requests.post(
            config["base_url"],
            json=payload,
            timeout=config["timeout"],
            headers=config["headers"]
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"Response: {content[:100]}...")
                
                if "AgentRouter connection successful" in content:
                    print("SUCCESS: AgentRouter connection successful!")
                    print("SUCCESS: GLM-4.6 is working correctly")
                    print("SUCCESS: PSnapBOT is ready to use!")
                    return True
                else:
                    print("WARNING: API responded but unexpected content")
                    print(f"WARNING: Content: {content}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return False
        elif response.status_code == 401:
            print("ERROR: Authentication failed")
            print("ERROR: Check your API key")
            print("ERROR: You may need to join AgentRouter Discord")
            return False
        elif response.status_code == 429:
            print("WARNING: Rate limit hit")
            print("WARNING: Please wait and try again")
            return False
        else:
            print(f"HTTP error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def main():
    """Run AgentRouter API test"""
    print("PSnapBOT AgentRouter API Test")
    print("=" * 50)
    
    # Test API connection
    if test_agentrouter_api():
        print("\n" + "=" * 50)
        print("All tests passed! PSnapBOT is ready to use!")
        print("\nTo start PSnapBOT:")
        print("  run_psnappbot.bat")
        print("\nOr run directly:")
        print('  "C:\\Users\\cntt.tts13\\AppData\\Local\\Programs\\Python\\Launcher\\py.exe" main.py')
        return 0
    else:
        print("\n" + "=" * 50)
        print("AgentRouter API connection test failed!")
        print("\nPossible solutions:")
        print("1. Check your API key")
        print("2. Join AgentRouter Discord for support")
        print("3. Check internet connection")
        print("4. Try again later")
        return 1

if __name__ == "__main__":
    sys.exit(main())