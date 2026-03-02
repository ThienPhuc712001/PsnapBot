"""
Planner for PSnapBOT - Local Persistent Development Agent
Handles decision making and action planning
"""
import re
from typing import Dict, Any, List, Optional
from agent.memory import MemorySystem
from agent.tools import ToolExecutor


class Planner:
    def __init__(self, memory: MemorySystem, tools: ToolExecutor):
        self.memory = memory
        self.tools = tools
    
    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user request and determine the appropriate action plan
        
        Args:
            user_input: The user's input string
            
        Returns:
            Dictionary with analysis results and action plan
        """
        analysis = {
            "request_type": self._classify_request(user_input),
            "is_build_fix": self._is_build_fix_request(user_input),
            "is_git_operation": self._is_git_operation(user_input),
            "is_file_operation": self._is_file_operation(user_input),
            "is_search_request": self._is_search_request(user_input),
            "requires_context": self._requires_context(user_input),
            "urgency": self._assess_urgency(user_input)
        }
        
        # Get relevant context from memory
        context = self._gather_context(user_input, analysis)
        
        # Create action plan
        action_plan = self._create_action_plan(user_input, analysis, context)
        
        return {
            "analysis": analysis,
            "context": context,
            "action_plan": action_plan
        }
    
    def _classify_request(self, user_input: str) -> str:
        """Classify the type of user request"""
        user_input_lower = user_input.lower()
        
        # Build fix requests
        if any(keyword in user_input_lower for keyword in ['fix build', 'build error', 'compile error', 'build failed']):
            return "build_fix"
        
        # Feature development
        if any(keyword in user_input_lower for keyword in ['add', 'implement', 'create', 'develop', 'build']):
            return "feature_development"
        
        # Code analysis
        if any(keyword in user_input_lower for keyword in ['explain', 'analyze', 'review', 'understand']):
            return "code_analysis"
        
        # Refactoring
        if any(keyword in user_input_lower for keyword in ['refactor', 'restructure', 'reorganize', 'clean up']):
            return "refactoring"
        
        # Testing
        if any(keyword in user_input_lower for keyword in ['test', 'testing', 'unit test', 'integration test']):
            return "testing"
        
        # Documentation
        if any(keyword in user_input_lower for keyword in ['document', 'docs', 'readme', 'comment']):
            return "documentation"
        
        # Git operations
        if user_input_lower.startswith('git ') or any(keyword in user_input_lower for keyword in ['commit', 'push', 'pull', 'branch', 'merge']):
            return "git_operation"
        
        # File operations
        if any(keyword in user_input_lower for keyword in ['read', 'write', 'create file', 'delete file', 'modify']):
            return "file_operation"
        
        # Search
        if any(keyword in user_input_lower for keyword in ['search', 'find', 'locate', 'where is']):
            return "search"
        
        # General inquiry
        return "general_inquiry"
    
    def _is_build_fix_request(self, user_input: str) -> bool:
        """Check if this is a build fix request"""
        build_keywords = [
            'fix build', 'build error', 'compile error', 'build failed',
            'compilation failed', 'build broken', 'wont build', 'cannot build'
        ]
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in build_keywords)
    
    def _is_git_operation(self, user_input: str) -> bool:
        """Check if this is a git operation"""
        git_keywords = ['git ', 'commit', 'push', 'pull', 'branch', 'merge', 'checkout', 'clone']
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in git_keywords)
    
    def _is_file_operation(self, user_input: str) -> bool:
        """Check if this involves file operations"""
        file_keywords = ['read', 'write', 'create', 'delete', 'modify', 'edit', 'file']
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in file_keywords)
    
    def _is_search_request(self, user_input: str) -> bool:
        """Check if this is a search request"""
        search_keywords = ['search', 'find', 'locate', 'where is', 'look for']
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in search_keywords)
    
    def _requires_context(self, user_input: str) -> bool:
        """Check if the request requires additional context"""
        context_needing_requests = [
            'explain', 'analyze', 'review', 'understand', 'fix', 'debug',
            'refactor', 'improve', 'optimize'
        ]
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in context_needing_requests)
    
    def _assess_urgency(self, user_input: str) -> str:
        """Assess the urgency of the request"""
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'blocking']
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in urgent_keywords):
            return "high"
        elif any(keyword in user_input_lower for keyword in ['when you can', 'sometime', 'eventually']):
            return "low"
        else:
            return "normal"
    
    def _gather_context(self, user_input: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Gather relevant context from memory and project"""
        context = {}
        
        # Get recent sessions if context is needed
        if analysis.get("requires_context", False):
            context["recent_sessions"] = self.memory.get_recent_sessions(limit=5)
        
        # For build fix requests, look for similar errors
        if analysis.get("is_build_fix", False):
            context["similar_errors"] = self.memory.find_similar_build_errors(user_input, limit=3)
        
        # Get project knowledge
        context["project_knowledge"] = self.memory.get_all_knowledge()
        
        # Detect project type
        project_info = self.tools.detect_project_type()
        context["project_type"] = project_info.get("type", "unknown")
        
        return context
    
    def _create_action_plan(self, user_input: str, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a step-by-step action plan"""
        request_type = analysis["request_type"]
        action_plan = []
        
        if request_type == "build_fix":
            action_plan = self._create_build_fix_plan(user_input, context)
        elif request_type == "feature_development":
            action_plan = self._create_feature_development_plan(user_input, context)
        elif request_type == "code_analysis":
            action_plan = self._create_code_analysis_plan(user_input, context)
        elif request_type == "refactoring":
            action_plan = self._create_refactoring_plan(user_input, context)
        elif request_type == "testing":
            action_plan = self._create_testing_plan(user_input, context)
        elif request_type == "git_operation":
            action_plan = self._create_git_operation_plan(user_input, context)
        elif request_type == "search":
            action_plan = self._create_search_plan(user_input, context)
        else:
            action_plan = self._create_general_plan(user_input, context)
        
        return action_plan
    
    def _create_build_fix_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for build fixes"""
        plan = [
            {
                "step": 1,
                "action": "detect_project_type",
                "description": "Detect project type to determine build command"
            },
            {
                "step": 2,
                "action": "run_build",
                "description": "Run the appropriate build command"
            }
        ]
        
        # If similar errors exist, suggest reviewing them first
        if context.get("similar_errors"):
            plan.insert(0, {
                "step": 1,
                "action": "review_similar_errors",
                "description": "Review similar past errors and their fixes"
            })
            # Renumber subsequent steps
            for i, step in enumerate(plan[1:], 2):
                step["step"] = i
        
        plan.extend([
            {
                "step": len(plan) + 1,
                "action": "analyze_error",
                "description": "Analyze build error output"
            },
            {
                "step": len(plan) + 1,
                "action": "read_related_files",
                "description": "Read files related to the error"
            },
            {
                "step": len(plan) + 1,
                "action": "apply_fix",
                "description": "Apply targeted fix to resolve the error"
            },
            {
                "step": len(plan) + 1,
                "action": "verify_fix",
                "description": "Run build again to verify the fix"
            },
            {
                "step": len(plan) + 1,
                "action": "save_fix",
                "description": "Save successful fix to memory"
            }
        ])
        
        return plan
    
    def _create_feature_development_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for feature development"""
        return [
            {
                "step": 1,
                "action": "analyze_requirements",
                "description": "Analyze feature requirements and scope"
            },
            {
                "step": 2,
                "action": "search_existing_code",
                "description": "Search for related existing code"
            },
            {
                "step": 3,
                "action": "design_implementation",
                "description": "Design the implementation approach"
            },
            {
                "step": 4,
                "action": "implement_feature",
                "description": "Implement the new feature"
            },
            {
                "step": 5,
                "action": "test_implementation",
                "description": "Test the implementation"
            },
            {
                "step": 6,
                "action": "document_changes",
                "description": "Document the changes made"
            }
        ]
    
    def _create_code_analysis_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for code analysis"""
        return [
            {
                "step": 1,
                "action": "identify_target",
                "description": "Identify what needs to be analyzed"
            },
            {
                "step": 2,
                "action": "read_files",
                "description": "Read relevant files for analysis"
            },
            {
                "step": 3,
                "action": "analyze_structure",
                "description": "Analyze code structure and patterns"
            },
            {
                "step": 4,
                "action": "provide_insights",
                "description": "Provide analysis and insights"
            }
        ]
    
    def _create_refactoring_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for refactoring"""
        return [
            {
                "step": 1,
                "action": "identify_refactor_target",
                "description": "Identify code to be refactored"
            },
            {
                "step": 2,
                "action": "analyze_current_code",
                "description": "Analyze current code structure"
            },
            {
                "step": 3,
                "action": "plan_refactoring",
                "description": "Plan the refactoring approach"
            },
            {
                "step": 4,
                "action": "apply_refactoring",
                "description": "Apply refactoring changes"
            },
            {
                "step": 5,
                "action": "test_refactored_code",
                "description": "Test refactored code"
            }
        ]
    
    def _create_testing_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for testing"""
        return [
            {
                "step": 1,
                "action": "identify_test_target",
                "description": "Identify what needs to be tested"
            },
            {
                "step": 2,
                "action": "run_existing_tests",
                "description": "Run existing tests"
            },
            {
                "step": 3,
                "action": "analyze_results",
                "description": "Analyze test results"
            },
            {
                "step": 4,
                "action": "create_or_fix_tests",
                "description": "Create new tests or fix existing ones"
            }
        ]
    
    def _create_git_operation_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for git operations"""
        return [
            {
                "step": 1,
                "action": "validate_git_command",
                "description": "Validate and prepare git command"
            },
            {
                "step": 2,
                "action": "execute_git_command",
                "description": "Execute the git command"
            },
            {
                "step": 3,
                "action": "verify_result",
                "description": "Verify the git operation result"
            }
        ]
    
    def _create_search_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create action plan for search operations"""
        return [
            {
                "step": 1,
                "action": "extract_search_terms",
                "description": "Extract search terms from request"
            },
            {
                "step": 2,
                "action": "execute_search",
                "description": "Search through codebase"
            },
            {
                "step": 3,
                "action": "present_results",
                "description": "Present and analyze search results"
            }
        ]
    
    def _create_general_plan(self, user_input: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a general action plan"""
        return [
            {
                "step": 1,
                "action": "understand_request",
                "description": "Understand and clarify the request"
            },
            {
                "step": 2,
                "action": "gather_information",
                "description": "Gather necessary information"
            },
            {
                "step": 3,
                "action": "provide_response",
                "description": "Provide appropriate response or take action"
            }
        ]