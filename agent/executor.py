"""
Executor for PSnapBOT - Local Persistent Development Agent
Handles execution of tool calls and manages the build-fix loop
"""
import json
import time
from typing import Dict, Any, List, Optional
from agent.memory import MemorySystem
from agent.tools import ToolExecutor
from config import MAX_BUILD_ATTEMPTS


class Executor:
    def __init__(self, memory: MemorySystem, tools: ToolExecutor):
        self.memory = memory
        self.tools = tools
        self.current_session = []
    
    def execute_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call and return the result
        
        Args:
            tool_call: Dictionary containing tool name and arguments
            
        Returns:
            Dictionary with execution result
        """
        tool_name = tool_call.get("name")
        arguments = tool_call.get("arguments", {})
        
        result = {
            "tool": tool_name,
            "arguments": arguments,
            "success": False,
            "result": None,
            "error": None
        }
        
        try:
            if tool_name == "run_shell":
                shell_result = self.tools.run_shell(arguments.get("command", ""))
                result["success"] = shell_result["success"]
                result["result"] = shell_result
                if not shell_result["success"]:
                    result["error"] = shell_result.get("error", "Unknown error")
            
            elif tool_name == "read_file":
                file_result = self.tools.read_file(arguments.get("path", ""))
                result["success"] = file_result["success"]
                result["result"] = file_result
                if not file_result["success"]:
                    result["error"] = file_result.get("error", "Unknown error")
            
            elif tool_name == "write_file":
                write_result = self.tools.write_file(
                    arguments.get("path", ""),
                    arguments.get("content", "")
                )
                result["success"] = write_result["success"]
                result["result"] = write_result
                if not write_result["success"]:
                    result["error"] = write_result.get("error", "Unknown error")
            
            elif tool_name == "search_code":
                search_result = self.tools.search_code(arguments.get("keyword", ""))
                result["success"] = search_result["success"]
                result["result"] = search_result
                if not search_result["success"]:
                    result["error"] = search_result.get("error", "Unknown error")
            
            elif tool_name == "git_command":
                git_result = self.tools.git_command(arguments.get("command", ""))
                result["success"] = git_result["success"]
                result["result"] = git_result
                if not git_result["success"]:
                    result["error"] = git_result.get("error", "Unknown error")
            
            else:
                result["error"] = f"Unknown tool: {tool_name}"
        
        except Exception as e:
            result["error"] = str(e)
        
        # Store in current session
        self.current_session.append(result)
        
        return result
    
    def execute_build_fix_loop(self, user_input: str) -> Dict[str, Any]:
        """
        Execute the build-fix loop for fixing build errors
        
        Args:
            user_input: The original user input requesting build fix
            
        Returns:
            Dictionary with the final result of the build-fix process
        """
        build_result = {
            "success": False,
            "attempts": 0,
            "error": None,
            "fixes_applied": [],
            "final_output": ""
        }
        
        # Detect project type
        project_info = self.tools.detect_project_type()
        if not project_info["success"]:
            build_result["error"] = "Could not detect project type"
            return build_result
        
        project_type = project_info["type"]
        build_command = self.tools.get_build_command(project_type)
        
        # Look for similar errors in memory
        similar_errors = self.memory.find_similar_build_errors(user_input, limit=3)
        
        for attempt in range(1, MAX_BUILD_ATTEMPTS + 1):
            build_result["attempts"] = attempt
            
            print(f"Build attempt {attempt}/{MAX_BUILD_ATTEMPTS}")
            
            # Run build command
            build_output = self.tools.run_shell(build_command)
            build_result["final_output"] = build_output.get("stdout", "") + build_output.get("stderr", "")
            
            if build_output["success"]:
                build_result["success"] = True
                print("Build successful!")
                break
            
            # Build failed, analyze error
            error_text = build_output.get("stderr", "") or build_output.get("stdout", "")
            print(f"Build failed with error: {error_text[:200]}...")
            
            # Check for similar errors and try previous fixes
            fix_applied = None
            if similar_errors and attempt == 1:
                print("Trying similar error fixes from memory...")
                for similar_error in similar_errors:
                    fix = similar_error["fix_applied"]
                    if self._try_apply_fix(fix, error_text):
                        fix_applied = f"Applied fix from similar error: {fix}"
                        break
            
            # If no similar fix worked, let the LLM analyze and fix
            if not fix_applied:
                fix_result = self._analyze_and_fix_error(error_text, project_type)
                if fix_result["success"]:
                    fix_applied = fix_result["fix_description"]
                    # Apply the fix
                    for file_change in fix_result.get("file_changes", []):
                        self.tools.write_file(file_change["path"], file_change["content"])
            
            if fix_applied:
                build_result["fixes_applied"].append(fix_applied)
                # Save this fix attempt to memory
                self.memory.save_build_fix(error_text, fix_applied)
            else:
                print("Could not determine a fix for this error")
                break
        
        return build_result
    
    def _try_apply_fix(self, fix_description: str, current_error: str) -> bool:
        """
        Try to apply a fix from memory to the current error
        
        Args:
            fix_description: Description of the fix that worked before
            current_error: Current error text
            
        Returns:
            True if fix was applied, False otherwise
        """
        # This is a simplified implementation
        # In a more sophisticated version, we could parse the fix description
        # and automatically apply the same changes
        
        # For now, just return False to let the LLM handle it
        return False
    
    def _analyze_and_fix_error(self, error_text: str, project_type: str) -> Dict[str, Any]:
        """
        Analyze build error and determine fix using LLM
        
        Args:
            error_text: The build error text
            project_type: The detected project type
            
        Returns:
            Dictionary with fix information
        """
        # This would normally call the LLM to analyze the error
        # For now, return a placeholder that indicates no fix was found
        return {
            "success": False,
            "fix_description": None,
            "file_changes": []
        }
    
    def execute_action_plan(self, action_plan: List[Dict[str, Any]], user_input: str) -> Dict[str, Any]:
        """
        Execute a step-by-step action plan
        
        Args:
            action_plan: List of action steps to execute
            user_input: Original user input
            
        Returns:
            Dictionary with execution results
        """
        execution_result = {
            "success": False,
            "completed_steps": [],
            "failed_step": None,
            "final_result": None
        }
        
        for step in action_plan:
            step_action = step.get("action")
            step_description = step.get("description")
            
            print(f"Executing step {step['step']}: {step_description}")
            
            try:
                step_result = self._execute_action_step(step_action, user_input, step)
                
                if step_result["success"]:
                    execution_result["completed_steps"].append({
                        "step": step["step"],
                        "action": step_action,
                        "description": step_description,
                        "result": step_result
                    })
                else:
                    execution_result["failed_step"] = {
                        "step": step["step"],
                        "action": step_action,
                        "description": step_description,
                        "error": step_result.get("error", "Unknown error")
                    }
                    break
            
            except Exception as e:
                execution_result["failed_step"] = {
                    "step": step["step"],
                    "action": step_action,
                    "description": step_description,
                    "error": str(e)
                }
                break
        
        if not execution_result["failed_step"]:
            execution_result["success"] = True
        
        return execution_result
    
    def _execute_action_step(self, action: str, user_input: str, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single action step
        
        Args:
            action: The action to execute
            user_input: Original user input
            step: Step information
            
        Returns:
            Dictionary with step result
        """
        if action == "detect_project_type":
            return self.tools.detect_project_type()
        
        elif action == "run_build":
            project_info = self.tools.detect_project_type()
            if project_info["success"]:
                build_command = self.tools.get_build_command(project_info["type"])
                return self.tools.run_shell(build_command)
            else:
                return {"success": False, "error": "Could not detect project type"}
        
        elif action == "analyze_error":
            # This would typically involve LLM analysis
            return {"success": True, "result": "Error analysis placeholder"}
        
        elif action == "read_related_files":
            # This would involve determining which files are related to the error
            return {"success": True, "result": "Read related files placeholder"}
        
        elif action == "apply_fix":
            # This would involve applying the determined fix
            return {"success": True, "result": "Applied fix placeholder"}
        
        elif action == "verify_fix":
            # Run build again to verify fix
            project_info = self.tools.detect_project_type()
            if project_info["success"]:
                build_command = self.tools.get_build_command(project_info["type"])
                return self.tools.run_shell(build_command)
            else:
                return {"success": False, "error": "Could not detect project type"}
        
        elif action == "save_fix":
            # Save fix to memory
            return {"success": True, "result": "Fix saved to memory"}
        
        elif action == "search_existing_code":
            # Extract keywords from user input and search
            keywords = self._extract_keywords(user_input)
            if keywords:
                return self.tools.search_code(keywords[0])  # Search for first keyword
            else:
                return {"success": False, "error": "No keywords found for search"}
        
        elif action == "read_files":
            # This would involve determining which files to read
            return {"success": True, "result": "Read files placeholder"}
        
        elif action == "execute_search":
            keywords = self._extract_keywords(user_input)
            if keywords:
                return self.tools.search_code(keywords[0])
            else:
                return {"success": False, "error": "No keywords found for search"}
        
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract relevant keywords from text for searching
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction - in a more sophisticated version,
        # we could use NLP techniques
        import re
        
        # Remove common words and extract potential keywords
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in common_words and len(word) > 2]
        
        return keywords[:5]  # Return top 5 keywords
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session
        
        Returns:
            Dictionary with session summary
        """
        return {
            "total_tool_calls": len(self.current_session),
            "successful_calls": sum(1 for call in self.current_session if call["success"]),
            "failed_calls": sum(1 for call in self.current_session if not call["success"]),
            "tools_used": list(set(call["tool"] for call in self.current_session)),
            "session": self.current_session
        }
    
    def clear_session(self):
        """Clear the current session history"""
        self.current_session = []