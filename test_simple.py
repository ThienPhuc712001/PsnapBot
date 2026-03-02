#!/usr/bin/env python3
"""
Simple test script to verify PSnapBOT
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from agent.memory import MemorySystem
        from agent.tools import ToolExecutor
        from agent.llm import LLMClient
        from agent.planner import Planner
        from agent.executor import Executor
        from agent.core import DevAgent
        print("All modules imported successfully")
        return True
    except Exception as e:
        print(f"Import error: {str(e)}")
        return False

def test_memory():
    """Test memory system"""
    try:
        from agent.memory import MemorySystem
        memory = MemorySystem()
        
        # Test saving and retrieving knowledge
        memory.save_knowledge("test_key", "test_value")
        value = memory.get_knowledge("test_key")
        
        if value == "test_value":
            print("Memory system working correctly")
            return True
        else:
            print("Memory system test failed")
            return False
    except Exception as e:
        print(f"Memory system error: {str(e)}")
        return False

def test_tools():
    """Test tool system"""
    try:
        from agent.tools import ToolExecutor
        tools = ToolExecutor()
        
        # Test project detection
        project_info = tools.detect_project_type()
        print(f"Project detection working: {project_info.get('type', 'unknown')}")
        
        # Test search (should work even if no results)
        search_result = tools.search_code("test")
        print(f"Search working: found {search_result.get('total_matches', 0)} matches")
        
        return True
    except Exception as e:
        print(f"Tools system error: {str(e)}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    try:
        from agent.core import DevAgent
        agent = DevAgent()
        print("Agent initialized successfully")
        return True
    except Exception as e:
        print(f"Agent initialization error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Testing PSnapBOT - Local Persistent Development Agent")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Memory System Test", test_memory),
        ("Tools System Test", test_tools),
        ("Agent Initialization Test", test_agent_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   WARNING: {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The agent is ready to use.")
        print("\nTo start the agent, run:")
        print("  \"C:\\Users\\cntt.tts13\\AppData\\Local\\Programs\\Python\\Launcher\\py.exe\" main.py")
        print("\nOr use a single command:")
        print('  \"C:\\Users\\cntt.tts13\\AppData\\Local\\Programs\\Python\\Launcher\\py.exe\" main.py \"help\"')
    else:
        print("Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())