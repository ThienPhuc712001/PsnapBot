"""
User Configuration for PSnapBOT
Add your API settings here
"""
import os

# ==========================================
# API CONFIGURATION - PLEASE UPDATE
# ==========================================

# Your API Key (required if not using free endpoint)
API_KEY = "sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"

# Alternative API Base URL (if different from default)
API_BASE_URL = "http://127.0.0.1:6969/v1"

# Model to use
API_MODEL = "glm-4.6"

# Request timeout in seconds
API_TIMEOUT = 30

# Maximum retry attempts
API_MAX_RETRIES = 3

# ==========================================
# HOW TO USE:
# ==========================================

# 1. Replace YOUR_API_KEY_HERE with your actual API key
# 2. If using a different endpoint, update API_BASE_URL
# 3. Save this file
# 4. Run PSnapBOT normally

# ==========================================
# FREE USAGE:
# ==========================================

# If you don't have an API key, PSnapBOT will use
# the default AgentRouter endpoint which may have limitations
# but should work for basic testing

def get_api_config():
    """Get API configuration"""
    return {
        "api_key": API_KEY,
        "base_url": API_BASE_URL,
        "model": API_MODEL,
        "timeout": API_TIMEOUT,
        "max_retries": API_MAX_RETRIES
    }

def is_configured():
    """Check if API is properly configured"""
    return API_KEY != "YOUR_API_KEY_HERE"

def print_config_status():
    """Print current configuration status"""
    print("Current API Configuration:")
    print("=" * 30)
    
    if is_configured():
        print("Status: CONFIGURED")
        print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
        print(f"Endpoint: {API_BASE_URL}")
        print(f"Model: {API_MODEL}")
    else:
        print("Status: NOT CONFIGURED")
        print("API Key: YOUR_API_KEY_HERE")
        print(f"Endpoint: {API_BASE_URL}")
        print(f"Model: {API_MODEL}")
        print("\nTo configure:")
        print("1. Edit this file (config_user.py)")
        print("2. Replace YOUR_API_KEY_HERE with your actual API key")
        print("3. Save the file")
        print("4. Run PSnapBOT again")

if __name__ == "__main__":
    print_config_status()