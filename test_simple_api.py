#!/usr/bin/env python3
"""
Simple API test for PSnapBOT
"""
import requests
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import API_BASE_URL, API_MODEL, API_TIMEOUT

def test_simple_api():
    """Simple test of API connectivity"""
    print("Testing PSnapBOT API connection...")
    print("=" * 40)
    
    try:
        # Test API with a simple request
        payload = {
            "model": API_MODEL,
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello, this is a test message. Please respond with 'API connection successful!'"
                }
            ],
            "max_tokens": 50
        }
        
        print(f"Connecting to: {API_BASE_URL}")
        print(f"Using model: {API_MODEL}")
        
        response = requests.post(
            API_BASE_URL,
            json=payload,
            timeout=API_TIMEOUT,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"Response: {content[:100]}...")
                
                if "API connection successful" in content:
                    print("API connection successful!")
                    print("GLM-4.6 is working correctly")
                    print("PSnapBOT is ready to use!")
                    return True
                else:
                    print("API responded but unexpected content")
                    print(f"Content: {content}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
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
    """Run simple API test"""
    print("PSnapBOT API Connection Test")
    print("=" * 40)
    
    # Test API connection
    if test_simple_api():
        print("\n" + "=" * 40)
        print("All tests passed! PSnapBOT is ready to use!")
        print("\nTo start PSnapBOT:")
        print("  run_psnappbot.bat")
        print("\nOr run directly:")
        print('  "C:\\Users\\cntt.tts13\\AppData\\Local\\Programs\\Python\\Launcher\\py.exe" main.py')
        return 0
    else:
        print("\n" + "=" * 40)
        print("API connection test failed!")
        print("\nPossible solutions:")
        print("1. Check internet connection")
        print("2. Verify firewall settings")
        print("3. Try again later")
        print("4. Check if AgentRouter is accessible")
        return 1

if __name__ == "__main__":
    sys.exit(main())