"""
Core Agent for PSnapBOT - Local Persistent Development Agent
Implements the main agent loop and coordinates all components
"""
import json
from typing import Dict, Any, List, Optional
from agent.memory import MemorySystem
from agent.llm import LLMClient
from agent.tools import ToolExecutor
from agent.planner import Planner
from agent.executor import Executor


class DevAgent:
    def __init__(self):
        """Initialize the development agent with all components"""
        self.memory = MemorySystem()
        self.llm = LLMClient()
        self.tools = ToolExecutor()
        self.planner = Planner(self.memory, self.tools)
        self.executor = Executor(self.memory, self.tools)
        
        self.conversation_history = []
        self.max_iterations = 10
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request through the complete agent loop
        
        Args:
            user_input: The user's input string
            
        Returns:
            Dictionary with the final response and metadata
        """
        print(f"Processing request: {user_input}")
        
        # Save user input to memory
        session_id = self.memory.save_session(user_input, "")
        
        # Analyze the request and create action plan
        planning_result = self.planner.analyze_request(user_input)
        
        # Handle build fix requests specially
        if planning_result["analysis"]["is_build_fix"]:
            result = self._handle_build_fix(user_input, planning_result)
        else:
            result = self._handle_general_request(user_input, planning_result)
        
        # Save the complete interaction to memory
        self.memory.save_session(user_input, json.dumps(result, indent=2))
        
        # Clear executor session
        self.executor.clear_session()
        
        return result
    
    def _handle_build_fix(self, user_input: str, planning_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle build fix requests with the specialized build-fix loop
        
        Args:
            user_input: The user's input requesting build fix
            planning_result: Result from the planner
            
        Returns:
            Dictionary with the build fix result
        """
        print("Initiating build-fix loop...")
        
        # Execute the build-fix loop
        build_result = self.executor.execute_build_fix_loop(user_input)
        
        # Format the response
        if build_result["success"]:
            response = {
                "success": True,
                "message": f"Build fixed successfully after {build_result['attempts']} attempts!",
                "details": {
                    "attempts": build_result["attempts"],
                    "fixes_applied": build_result["fixes_applied"],
                    "final_output": build_result["final_output"][:1000] + "..." if len(build_result["final_output"]) > 1000 else build_result["final_output"]
                }
            }
        else:
            response = {
                "success": False,
                "message": f"Could not fix build after {build_result['attempts']} attempts",
                "details": {
                    "attempts": build_result["attempts"],
                    "fixes_applied": build_result["fixes_applied"],
                    "final_error": build_result["final_output"][:1000] + "..." if len(build_result["final_output"]) > 1000 else build_result["final_output"]
                }
            }
        
        return response
    
    def _handle_general_request(self, user_input: str, planning_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle general requests using the LLM and tool execution loop
        
        Args:
            user_input: The user's input
            planning_result: Result from the planner
            
        Returns:
            Dictionary with the response
        """
        # Create conversation context
        context = planning_result["context"]
        system_prompt = self.llm.create_system_prompt(context)
        
        # Initialize conversation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # Get tool definitions
        tools = self.llm.create_tool_definitions()
        
        # Agent loop
        for iteration in range(self.max_iterations):
            print(f"Agent iteration {iteration + 1}/{self.max_iterations}")
            
            # Get LLM response
            try:
                llm_response = self.llm.chat_completion(messages, tools)
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Error communicating with LLM: {str(e)}",
                    "iterations": iteration + 1
                }
            
            # Check for tool call
            tool_call = self.llm.extract_tool_call(llm_response)
            
            if tool_call:
                # Execute tool call
                tool_result = self.executor.execute_tool_call(tool_call)
                
                # Add tool result to conversation
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": f"call_{iteration}",
                        "type": "function",
                        "function": {
                            "name": tool_call["name"],
                            "arguments": json.dumps(tool_call["arguments"])
                        }
                    }]
                })
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": f"call_{iteration}",
                    "content": json.dumps(tool_result)
                })
                
                # Continue loop for next iteration
                continue
            
            else:
                # No tool call, get final response
                content = self.llm.extract_content(llm_response)
                
                return {
                    "success": True,
                    "message": content,
                    "iterations": iteration + 1,
                    "session_summary": self.executor.get_session_summary()
                }
        
        # Max iterations reached
        return {
            "success": False,
            "message": "Maximum iterations reached without completion",
            "iterations": self.max_iterations,
            "session_summary": self.executor.get_session_summary()
        }
    
    def interactive_mode(self) -> None:
        """
        Run the agent in interactive CLI mode
        """
        print("PSnapBOT - Local Persistent Development Agent")
        print("Type 'help' for commands, 'exit' to quit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye! 👋")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'status':
                    self._show_status()
                    continue
                
                if user_input.lower() == 'history':
                    self._show_history()
                    continue
                
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("Conversation history cleared.")
                    continue
                
                # Process the request
                print("Processing...")
                result = self.process_request(user_input)
                
                # Display result
                if result["success"]:
                    print(f"SUCCESS: {result['message']}")
                else:
                    print(f"ERROR: {result['message']}")
                
                # Show additional details if available
                if "details" in result:
                    print("\nDetails:")
                    for key, value in result["details"].items():
                        if isinstance(value, list):
                            print(f"  {key}:")
                            for item in value:
                                print(f"    - {item}")
                        else:
                            print(f"  {key}: {value}")
                
                print()
            
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _show_help(self) -> None:
        """Show help information"""
        help_text = """
Available commands:
  help     - Show this help message
  status   - Show agent status and statistics
  history  - Show recent conversation history
  clear    - Clear conversation history
  exit     - Exit the agent

Example requests:
  "fix build" - Fix build errors in the project
  "add login feature" - Implement a new login feature
  "explain project structure" - Analyze and explain the project
  "search for user authentication" - Search for authentication code
  "refactor user service" - Refactor the user service module
  "run tests" - Execute project tests
        """
        print(help_text)
    
    def _show_status(self) -> None:
        """Show agent status and statistics"""
        # Get project info
        project_info = self.tools.detect_project_type()
        
        # Get memory statistics
        recent_sessions = self.memory.get_recent_sessions(limit=10)
        all_knowledge = self.memory.get_all_knowledge()
        
        print(f"""
Agent Status:
=============
Project Type: {project_info.get('type', 'Unknown')}
Project Root: {self.tools.project_root}

Memory Statistics:
- Recent Sessions: {len(recent_sessions)}
- Knowledge Items: {len(all_knowledge)}
- Database Path: {self.memory.db_path}

Current Session:
- Tool Calls: {len(self.executor.current_session)}
- Successful: {sum(1 for call in self.executor.current_session if call['success'])}
- Failed: {sum(1 for call in self.executor.current_session if not call['success'])}
        """)
    
    def _show_history(self) -> None:
        """Show recent conversation history"""
        recent_sessions = self.memory.get_recent_sessions(limit=5)
        
        if not recent_sessions:
            print("No recent conversation history.")
            return
        
        print("Recent Conversation History:")
        print("=" * 40)
        
        for i, session in enumerate(recent_sessions, 1):
            print(f"\n{i}. User: {session['user_input'][:80]}{'...' if len(session['user_input']) > 80 else ''}")
            print(f"   Time: {session['timestamp']}")
            if session['agent_response']:
                response_preview = session['agent_response'][:100] + "..." if len(session['agent_response']) > 100 else session['agent_response']
                print(f"   Agent: {response_preview}")
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the agent
        
        Returns:
            Dictionary with agent information
        """
        return {
            "name": "PSnapBOT",
            "version": "1.0.0",
            "components": {
                "memory": "SQLite-based memory system",
                "llm": "GLM-4.6 via AgentRouter",
                "tools": "Shell, File, Search, Git operations",
                "planner": "Request analysis and action planning",
                "executor": "Tool execution and build-fix loop"
            },
            "capabilities": [
                "Build error fixing",
                "Feature development",
                "Code analysis",
                "Refactoring",
                "Testing",
                "Git operations",
                "Code search",
                "Documentation"
            ],
            "safety_features": [
                "Restricted shell commands",
                "Project directory confinement",
                "Dangerous command blocking",
                "Git push confirmation",
                "Memory-based learning"
            ]
        }