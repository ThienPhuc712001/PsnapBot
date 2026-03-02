"""
LLM Integration for PSnapBOT - Local Persistent Development Agent
Handles communication with GLM-4.6 via AgentRouter API
"""
import requests
import json
import time
from typing import List, Dict, Any, Optional
from config_agentrouter import get_agentrouter_config, get_headers


class LLMClient:
    def __init__(self):
        config = get_agentrouter_config()
        self.base_url = config['base_url']
        self.model = config['model']
        self.timeout = config['timeout']
        self.max_retries = config['max_retries']
        self.api_key = config['api_key']
    
    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Send a chat completion request to GLM-4.6
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions
            
        Returns:
            Response dictionary from the API
        """
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        if tools:
            payload["tools"] = tools
        
        for attempt in range(self.max_retries):
            try:
                headers = get_headers()
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    timeout=self.timeout,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to connect to API after {self.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def extract_tool_call(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract tool call information from API response
        
        Args:
            response: API response dictionary
            
        Returns:
            Tool call dictionary or None if no tool call
        """
        try:
            choices = response.get("choices", [])
            if not choices:
                return None
            
            message = choices[0].get("message", {})
            tool_calls = message.get("tool_calls", [])
            
            if not tool_calls:
                return None
            
            tool_call = tool_calls[0]
            function = tool_call.get("function", {})
            
            return {
                "name": function.get("name"),
                "arguments": json.loads(function.get("arguments", "{}"))
            }
        
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Error extracting tool call: {str(e)}")
            return None
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """
        Extract text content from API response
        
        Args:
            response: API response dictionary
            
        Returns:
            Content string
        """
        try:
            choices = response.get("choices", [])
            if not choices:
                return ""
            
            message = choices[0].get("message", {})
            return message.get("content", "")
        
        except (KeyError, IndexError):
            return ""
    
    def create_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """
        Create the system prompt for the agent
        
        Args:
            context: Optional context dictionary with relevant information
            
        Returns:
            System prompt string
        """
        base_prompt = """You are a senior software engineer and autonomous development agent.

Your task is to help develop multi-language software projects by:
1. Analyzing user requests step by step
2. Using tools to gather information and make changes
3. Providing clear, actionable responses
4. Learning from previous fixes stored in memory

IMPORTANT RULES:
- Always read files before modifying them
- Always verify build after applying fixes
- Prefer tool calls over guessing file contents
- Never hallucinate file content or structure
- Use search_code() before reading files to locate relevant code
- Learn from previous fixes stored in memory
- Reason step by step before taking action

SAFETY RULES:
- Never delete entire project folders
- Never run system-wide destructive commands
- Restrict shell operations to project root only
- Ask for confirmation before git push operations

When fixing build errors:
1. Detect project type and run appropriate build command
2. Analyze errors carefully
3. Read related files to understand context
4. Apply targeted fixes
5. Build again to verify
6. Save successful fixes in memory

You have access to the following tools:
- run_shell: Execute shell commands safely
- read_file: Read file contents
- write_file: Write or modify files
- search_code: Search for code patterns
- git_command: Execute git commands

Always respond with tool calls when you need to interact with the project, and provide explanations when you have completed the task."""
        
        if context:
            if "recent_sessions" in context:
                base_prompt += f"\n\nRecent Sessions:\n{json.dumps(context['recent_sessions'], indent=2)}"
            
            if "similar_errors" in context:
                base_prompt += f"\n\nSimilar Past Errors:\n{json.dumps(context['similar_errors'], indent=2)}"
            
            if "project_knowledge" in context:
                base_prompt += f"\n\nProject Knowledge:\n{json.dumps(context['project_knowledge'], indent=2)}"
        
        return base_prompt
    
    def create_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Create tool definitions for the LLM
        
        Returns:
            List of tool definition dictionaries
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "run_shell",
                    "description": "Execute a shell command safely in the project directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "The shell command to execute"
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The file path to read"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write or modify a file with new content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "The file path to write"
                            },
                            "content": {
                                "type": "string",
                                "description": "The content to write to the file"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_code",
                    "description": "Search for code patterns in the project",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "The keyword or pattern to search for"
                            }
                        },
                        "required": ["keyword"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_command",
                    "description": "Execute git commands safely",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "The git command to execute (without 'git' prefix)"
                            }
                        },
                        "required": ["command"]
                    }
                }
            }
        ]