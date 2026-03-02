#!/usr/bin/env python3
"""
Direct test of PSnapBOT LLM client
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from agent.llm import LLMClient
    
    print("Testing PSnapBOT LLM Client directly...")
    
    # Initialize LLM client
    llm = LLMClient()
    
    print(f"Base URL: {llm.base_url}")
    print(f"Model: {llm.model}")
    print(f"API Key: {llm.api_key[:20]}...{llm.api_key[-10:]}")
    
    # Test simple chat completion
    messages = [
        {"role": "user", "content": "Hello, respond with just 'Working'"}
    ]
    
    print("\nSending request...")
    print(f"URL: {llm.base_url}/chat/completions")
    
    response = llm.chat_completion(messages)
    
    print(f"Response: {response}")
    
    if 'choices' in response and len(response['choices']) > 0:
        content = response['choices'][0]['message']['content']
        print(f"\n[SUCCESS] LLM Response: {content}")
    else:
        print(f"[ERROR] Unexpected response format")
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed.")