#!/usr/bin/env python3
"""
PSnapBOT Success Test - Final verification
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("PSnapBOT - Local Persistent Development Agent")
print("Final System Test")
print("=" * 50)

try:
    # Test core imports
    from agent.memory import MemorySystem
    from agent.tools import ToolExecutor
    from agent.planner import Planner
    from agent.executor import Executor
    from agent.core import DevAgent
    
    print("[OK] All core modules imported successfully")
    
    # Test initialization
    memory = MemorySystem()
    tools = ToolExecutor()
    planner = Planner(memory, tools)
    executor = Executor(memory, tools)
    agent = DevAgent()
    
    print("[OK] All systems initialized successfully")
    
    # Test basic functionality
    memory.save_session("test_input", "test_response")
    print("[OK] Memory system operational")
    
    agent_info = agent.get_agent_info()
    print(f"[OK] Agent: {agent_info['name']} v{agent_info['version']}")
    
    project_info = tools.detect_project_type()
    print(f"[OK] Project detection: {project_info['type']}")
    
    # Test configuration
    try:
        from config_agentrouter import get_agentrouter_config
        config = get_agentrouter_config()
        if config['api_key']:
            print("[OK] API configuration found")
        else:
            print("[WARNING] API key not configured")
    except:
        print("[WARNING] Configuration check failed")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] PSnapBOT TEST SUCCESSFUL!")
    print("[INFO] Your Local Persistent Development Agent is ready!")
    print("=" * 50)
    
    print("\nTo run PSnapBOT:")
    print("1. Interactive mode: py main.py")
    print("2. Single command: py main.py \"your request\"")
    print("3. Use run_psnappbot.bat for easy startup")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed.")