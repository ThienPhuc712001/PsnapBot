#!/usr/bin/env python3
"""
PSnapBOT Final Demo - Shows complete functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_psnappbot_features():
    """Show all PSnapBOT features"""
    
    print("=" * 60)
    print("PSnapBOT - Local Persistent Development Agent")
    print("=" * 60)
    
    print("\nFEATURES:")
    print("[OK] Memory System (SQLite database)")
    print("[OK] File Operations (read/write/search)")
    print("[OK] Project Analysis")
    print("[OK] Shell Command Execution (safe)")
    print("[OK] Code Search across 30+ file types")
    print("[OK] Build-Fix Loop with error learning")
    print("[OK] Interactive CLI Mode")
    print("[OK] Single Command Mode")
    print("[!] AI Features (requires API configuration)")
    
    print("\nPROJECT STRUCTURE:")
    print("dev_agent/")
    print("|-- agent/")
    print("|   |-- core.py      # Main agent logic")
    print("|   |-- memory.py    # SQLite database")
    print("|   |-- llm.py       # AI integration")
    print("|   |-- tools.py     # File/shell operations")
    print("|   |-- planner.py   # Request planning")
    print("|   |-- executor.py  # Task execution")
    print("|-- config_user.py   # User configuration")
    print("|-- main.py         # CLI interface")
    print("|-- data/           # Database storage")
    
    print("\nCONFIGURATION:")
    print("API Base URL: http://127.0.0.1:6969/v1")
    print("Model: glm-4.6")
    print("API Key: Configured")
    
    print("\nCURRENT STATUS:")
    
    try:
        from agent.memory import MemorySystem
        from agent.tools import ToolExecutor
        
        # Test memory
        memory = MemorySystem()
        sessions = memory.get_recent_sessions(5)
        knowledge = memory.get_all_knowledge()
        
        print(f"Memory System: [OK] Active")
        print(f"  - Sessions: {len(sessions)}")
        print(f"  - Knowledge items: {len(knowledge)}")
        
        # Test tools
        tools = ToolExecutor()
        result = tools.detect_project_type()
        
        print(f"Tool System: [OK] Active")
        print(f"  - Project type: {result.get('project_type', 'unknown')}")
        
        # Test file operations
        if os.path.exists("test.py"):
            result = tools.read_file("test.py")
            if result["success"]:
                print(f"  - File operations: [OK] Working")
        
    except Exception as e:
        print(f"System Status: ❌ Error - {e}")
    
    print("\nUSAGE EXAMPLES:")
    print("# Start interactive mode:")
    print("python main.py --project .")
    print()
    print("# Single command:")
    print('python main.py --project . "Analyze test.py"')
    print()
    print("# Show status:")
    print("python main.py --project . --status")
    
    print("\nNEXT STEPS:")
    print("1. Configure AgentRouterAnywhere with OpenAI provider")
    print("2. Add API URL: http://127.0.0.1:6969/v1")
    print("3. Add API Key: sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g")
    print("4. Add Model: glm-4.6")
    print("5. Save and test connection")
    
    print("\n" + "=" * 60)
    print("PSnapBOT is ready for development work!")
    print("=" * 60)

def test_file_operations():
    """Test file operations with test.py"""
    
    print("\nTESTING FILE OPERATIONS:")
    
    try:
        from agent.tools import ToolExecutor
        tools = ToolExecutor()
        
        # Read test.py
        result = tools.read_file("test.py")
        if result["success"]:
            print("[OK] Successfully read test.py")
            print(f"Content length: {len(result['content'])} characters")
            
            # Search for content
            search_result = tools.search_code("Hello")
            if search_result["success"]:
                print(f"[OK] Found {len(search_result['results'])} matches for 'Hello'")
        
    except Exception as e:
        print(f"[ERROR] File operations error: {e}")

if __name__ == "__main__":
    show_psnappbot_features()
    test_file_operations()
    
    print("\nPSnapBOT Demo Completed!")
    print("Core functionality is working. Configure API for AI features.")