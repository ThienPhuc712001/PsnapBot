"""
LLM Integration for PSnapBOT - OpenAI Compatible Version
Handles communication with OpenAI-compatible APIs including OpenAI, AgentRouter, etc.
"""
import requests
import json
import time
from typing import List, Dict, Any, Optional


class LLMClientOpenAI:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1/chat/completions", model: str = "gpt-3.5-turbo"):
        """Initialize LLM client with OpenAI-compatible API"""
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = 30
        self.max_retries = 3
    
    def chat_completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenAI-compatible API
        
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
        
        # Add API key for OpenAI
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Add tools if provided
        if tools:
            payload["tools"] = tools
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout,
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception("Invalid API key or unauthorized access")
                elif response.status_code == 429:
                    print(f"Rate limit hit, waiting {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                    continue
                else:
                    print(f"HTTP error {response.status_code}: {response.text[:200]}")
                    if attempt == self.max_retries - 1:
                        raise Exception(f"Failed after {self.max_retries} attempts")
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed after {self.max_retries} attempts: {str(e)}")
                continue
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed after {self.max_retries} attempts: {str(e)}")
                continue
        
        raise Exception(f"All {self.max_retries} attempts failed")
    
    def extract_tool_call(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract tool call information from API response
        
        Args:
            response: API response dictionary
            
        Returns:
            Tool call dictionary or None
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