#!/usr/bin/env python3
"""
Test PSnapBOT offline functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("[OK] Testing PSnapBOT Core Components...")
    
    # Test memory system
    from agent.memory import MemorySystem
    memory = MemorySystem()
    print("[OK] Memory system initialized")
    
    # Test tools
    from agent.tools import ToolExecutor
    tools = ToolExecutor()
    print("[OK] Tool system initialized")
    
    # Test planner
    from agent.planner import Planner
    planner = Planner(memory, tools)
    print("[OK] Planner system initialized")
    
    # Test executor
    from agent.executor import Executor
    executor = Executor(memory, tools)
    print("[OK] Executor system initialized")
    
    # Test core agent (without LLM)
    from agent.core import DevAgent
    agent = DevAgent()
    print("[OK] DevAgent core initialized")
    
    print("\n=== Testing Memory Operations ===")
    
    # Test session creation
    session_id = memory.create_session("test_session")
    print(f"[OK] Created session: {session_id}")
    
    # Test storing knowledge
    memory.store_project_knowledge(
        key="test_file",
        project_type="python",
        file_path="test.py",
        content="print('Hello PSnapBOT')",
        description="Test file"
    )
    print("[OK] Stored project knowledge")
    
    # Test retrieving knowledge
    knowledge = memory.get_project_knowledge()
    print(f"[OK] Retrieved {len(knowledge)} knowledge items")
    
    # Test tools functionality
    print("\n=== Testing Tools ===")
    
    # Test file search
    search_results = tools.search_code_files(".", "*.py", limit=5)
    print(f"[OK] Found {len(search_results)} Python files")
    
    # Test project detection
    project_type = tools.detect_project_type(".")
    print(f"[OK] Detected project type: {project_type}")
    
    print("\n=== Testing Agent Info ===")
    agent_info = agent.get_agent_info()
    print(f"[OK] Agent Name: {agent_info['name']}")
    print(f"[OK] Agent Version: {agent_info['version']}")
    print(f"[OK] Agent Status: {agent_info['status']}")
    
    print("\n[SUCCESS] All PSnapBOT core components working correctly!")
    print("[INFO] PSnapBOT is ready for use with valid API credentials")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")