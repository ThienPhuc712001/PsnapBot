#!/usr/bin/env python3
"""
Test Authorization Header Fix for PSnapBOT
This test verifies that Authorization headers are not sent to local endpoints
"""

import sys
import os
import json
import requests
from unittest.mock import patch, MagicMock

# Add the dev_agent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.llm import LLMClient
from config_user import get_api_config

def test_authorization_header_logic():
    """Test that Authorization headers are handled correctly"""
    print("🔍 Testing Authorization Header Logic...")
    
    # Test 1: Local endpoint should not send Authorization header
    print("\n1️⃣ Testing local endpoint (should NOT send Authorization header)")
    local_client = LLMClient()
    local_client.base_url = "http://127.0.0.1:6969/v1"
    local_client.api_key = "test-key-123"
    
    # Mock the requests.post to capture headers
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "test"}}]}
        mock_post.return_value = mock_response
        
        try:
            local_client.chat_completion([{"role": "user", "content": "test"}])
            
            # Check what headers were sent
            call_args = mock_post.call_args
            headers = call_args[1]['headers']
            
            print(f"   Headers sent: {headers}")
            
            if 'Authorization' in headers:
                print("   ❌ FAIL: Authorization header was sent to local endpoint")
                return False
            else:
                print("   ✅ PASS: No Authorization header sent to local endpoint")
                
        except Exception as e:
            print(f"   ⚠️  Error during local test: {e}")
    
    # Test 2: Remote endpoint should send Authorization header
    print("\n2️⃣ Testing remote endpoint (should send Authorization header)")
    remote_client = LLMClient()
    remote_client.base_url = "https://agentrouter.org/v1"
    remote_client.api_key = "test-key-123"
    
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "test"}}]}
        mock_post.return_value = mock_response
        
        try:
            remote_client.chat_completion([{"role": "user", "content": "test"}])
            
            # Check what headers were sent
            call_args = mock_post.call_args
            headers = call_args[1]['headers']
            
            print(f"   Headers sent: {headers}")
            
            if 'Authorization' in headers:
                print("   ✅ PASS: Authorization header was sent to remote endpoint")
            else:
                print("   ❌ FAIL: Authorization header was NOT sent to remote endpoint")
                return False
                
        except Exception as e:
            print(f"   ⚠️  Error during remote test: {e}")
    
    return True

def test_actual_local_endpoint():
    """Test actual connection to local AgentRouterAnywhere"""
    print("\n🌐 Testing Actual Local Endpoint Connection...")
    
    config = get_api_config()
    print(f"   Base URL: {config['base_url']}")
    print(f"   Model: {config['model']}")
    
    # Create client with actual config
    client = LLMClient()
    
    # Test simple request
    messages = [{"role": "user", "content": "Hello, just say 'API working'"}]
    
    try:
        print("   Sending test request...")
        response = client.chat_completion(messages)
        
        if response and 'choices' in response:
            content = response['choices'][0]['message']['content']
            print(f"   ✅ Response received: {content[:100]}...")
            return True
        else:
            print(f"   ❌ Invalid response format: {response}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_request_headers_debug():
    """Debug test to show exactly what headers are being sent"""
    print("\n🔬 Debug: Analyzing Request Headers...")
    
    # Create custom session to log headers
    class LoggingSession(requests.Session):
        def request(self, method, url, **kwargs):
            headers = kwargs.get('headers', {})
            print(f"   📤 Request to: {url}")
            print(f"   📤 Headers: {json.dumps(headers, indent=2)}")
            return super().request(method, url, **kwargs)
    
    # Patch LLMClient to use our logging session
    original_post = requests.post
    
    def logging_post(url, **kwargs):
        session = LoggingSession()
        return session.post(url, **kwargs)
    
    with patch('requests.post', side_effect=logging_post):
        try:
            client = LLMClient()
            messages = [{"role": "user", "content": "test"}]
            
            print("   Testing with current configuration...")
            client.chat_completion(messages)
            
        except Exception as e:
            print(f"   Expected error for debug: {e}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 PSnapBOT Authorization Header Fix Test")
    print("=" * 60)
    
    # Test 1: Authorization header logic
    logic_test_passed = test_authorization_header_logic()
    
    # Test 2: Request headers debug
    test_request_headers_debug()
    
    # Test 3: Actual endpoint test
    if logic_test_passed:
        endpoint_test_passed = test_actual_local_endpoint()
    else:
        endpoint_test_passed = False
        print("\n⏭️  Skipping endpoint test due to logic test failure")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Authorization Header Logic: {'✅ PASS' if logic_test_passed else '❌ FAIL'}")
    print(f"Local Endpoint Connection: {'✅ PASS' if endpoint_test_passed else '❌ FAIL'}")
    
    if logic_test_passed and endpoint_test_passed:
        print("\n🎉 All tests passed! Authorization header fix is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())