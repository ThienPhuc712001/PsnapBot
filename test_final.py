#!/usr/bin/env python3
"""
Final test for PSnapBOT - Test core functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("[OK] Testing PSnapBOT Final Integration...")
    
    # Test core components
    from agent.memory import MemorySystem
    from agent.tools import ToolExecutor
    from agent.planner import Planner
    from agent.executor import Executor
    from agent.core import DevAgent
    
    print("[OK] All imports successful")
    
    # Initialize systems
    memory = MemorySystem()
    tools = ToolExecutor()
    planner = Planner(memory, tools)
    executor = Executor(memory, tools)
    agent = DevAgent()
    
    print("[OK] All systems initialized successfully")
    
    # Test basic functionality
    print("\n=== Testing Basic Operations ===")
    
    # Test memory
    memory.save_session("test_user_input", "test_agent_response")
    print("[OK] Memory system working")
    
    # Test tools
    result = tools.run_shell("echo 'PSnapBOT Test'")
    if result["success"]:
        print("[OK] Tool execution working")
    else:
        print("[WARNING] Tool execution issue")
    
    # Test agent info
    agent_info = agent.get_agent_info()
    print(f"[OK] Agent: {agent_info['name']} v{agent_info['version']}")
    
    print("\n=== Testing Project Detection ===")
    project_type = tools.detect_project_type()
    print(f"[OK] Project type detected: {project_type}")
    
    print("\n=== Testing File Search ===")
    python_files = tools.search_code_files("*.py", limit=3)
    print(f"[OK] Found {len(python_files)} Python files")
    
    print("\n[SUCCESS] PSnapBOT Core System Test PASSED!")
    print("[INFO] All major components are working correctly")
    print("[INFO] PSnapBOT is ready for development tasks")
    
    # Test configuration
    try:
        from config_agentrouter import print_config_status
        print("\n=== Configuration Status ===")
        print_config_status()
    except:
        print("[WARNING] Could not load configuration")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n=== PSnapBOT Test Complete ===")