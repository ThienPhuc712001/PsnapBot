"""
AgentRouter Configuration for PSnapBOT
Special configuration for AgentRouter API with GLM-4.6
"""
import os

# ==========================================
# AGENTROUTER CONFIGURATION
# ==========================================

# AgentRouter API Configuration
API_KEY = "sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"  # Leave empty if using their free tier
API_BASE_URL = "http://127.0.0.1:6969"
API_MODEL = "glm-4.6"
API_TIMEOUT = 60  # Longer timeout for AgentRouter
API_MAX_RETRIES = 5  # More retries for stability

# Special headers for AgentRouter
def get_headers():
    """Get headers for AgentRouter API"""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PSnapBOT/1.0.0"
    }
    
    # Add API key if available
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    return headers

# ==========================================
# HOW TO USE:
# ==========================================

# 1. If you have an AgentRouter API key, add it above
# 2. If using free tier, leave API_KEY empty
# 3. Update main.py to use this config instead of config.py

def get_agentrouter_config():
    """Get AgentRouter API configuration"""
    return {
        "api_key": API_KEY,
        "base_url": API_BASE_URL,
        "model": API_MODEL,
        "timeout": API_TIMEOUT,
        "max_retries": API_MAX_RETRIES,
        "headers": get_headers()
    }

def is_configured():
    """Check if AgentRouter API is properly configured"""
    # AgentRouter works with empty API key for free tier
    return True  # Always configured for AgentRouter

def print_config_status():
    """Print current AgentRouter configuration"""
    print("AgentRouter Configuration:")
    print("=" * 30)
    
    if API_KEY:
        print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    else:
        print("API Key: Using free tier (no key required)")
    
    print(f"Endpoint: {API_BASE_URL}")
    print(f"Model: {API_MODEL}")
    print(f"Timeout: {API_TIMEOUT}s")
    print(f"Max Retries: {API_MAX_RETRIES}")
    print("Status: CONFIGURED for AgentRouter")
    
    if not API_KEY:
        print("\nNote: Using AgentRouter free tier")
        print("This may have limitations but should work for testing")

if __name__ == "__main__":
    print_config_status()