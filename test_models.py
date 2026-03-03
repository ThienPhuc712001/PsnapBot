#!/usr/bin/env python3
"""
Test available models in AgentRouterAnywhere
"""
import requests
import json

def test_available_models():
    """Test to get available models from AgentRouterAnywhere"""
    
    print("Testing available models...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"
    }
    
    try:
        # Try to get models list
        response = requests.get(
            "http://127.0.0.1:6969/v1/models",
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            models = response.json()
            print("Available models:")
            for model in models.get('data', []):
                print(f"  - {model.get('id', 'Unknown')}")
            return True
        else:
            print("Failed to get models list")
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_with_different_models():
    """Test with different model names"""
    
    models_to_try = [
        "glm-4.6",
        "gpt-3.5-turbo",
        "gpt-4",
        "claude-3-sonnet",
        "llama-2",
        "text-davinci-003"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"
    }
    
    data = {
        "messages": [
            {"role": "user", "content": "Say 'Hello from model'"}
        ],
        "max_tokens": 20
    }
    
    for model in models_to_try:
        print(f"\nTesting with model: {model}")
        data["model"] = model
        
        try:
            response = requests.post(
                "http://127.0.0.1:6969/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"SUCCESS: {content}")
                return model, True
            else:
                print(f"FAILED: {response.text[:200]}...")
                
        except Exception as e:
            print(f"ERROR: {e}")
    
    return None, False

if __name__ == "__main__":
    print("=== AgentRouterAnywhere Model Test ===")
    
    # Test available models
    test_available_models()
    
    # Test with different models
    working_model, success = test_with_different_models()
    
    if success:
        print(f"\nSUCCESS: Working model found: {working_model}")
    else:
        print("\nFAILED: No working model found")
        print("Please configure AgentRouterAnywhere with proper provider settings")
    
    print("\nTest completed.")