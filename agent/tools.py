"""
Tools for PSnapBOT - Local Persistent Development Agent
Implements shell execution, file operations, code search, and git commands
"""
import subprocess
import os
import json
import glob
from typing import Dict, Any, List
from config import PROJECT_ROOT, SHELL_TIMEOUT, ALLOWED_SHELL_COMMANDS, DANGEROUS_COMMANDS


class ToolExecutor:
    def __init__(self):
        self.project_root = PROJECT_ROOT
    
    def run_shell(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command safely in the project directory
        
        Args:
            command: The shell command to execute
            
        Returns:
            Dictionary with success status, stdout, stderr, and exit_code
        """
        # Safety checks
        if self._is_dangerous_command(command):
            return {
                "success": False,
                "error": "Command blocked for safety reasons",
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        
        # Check if command starts with allowed command
        command_parts = command.strip().split()
        if not command_parts:
            return {
                "success": False,
                "error": "Empty command",
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        
        base_command = command_parts[0]
        if base_command not in ALLOWED_SHELL_COMMANDS and not command.startswith("git "):
            return {
                "success": False,
                "error": f"Command '{base_command}' is not allowed",
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        
        try:
            # Execute command in project directory
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=SHELL_TIMEOUT
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {SHELL_TIMEOUT} seconds",
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read the contents of a file
        
        Args:
            path: The file path to read
            
        Returns:
            Dictionary with success status and file content
        """
        try:
            # Normalize path and ensure it's within project root
            full_path = os.path.abspath(os.path.join(self.project_root, path))
            if not full_path.startswith(os.path.abspath(self.project_root)):
                return {
                    "success": False,
                    "error": "Access denied: Path is outside project directory",
                    "content": ""
                }
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": f"File not found: {path}",
                    "content": ""
                }
            
            if os.path.isdir(full_path):
                return {
                    "success": False,
                    "error": f"Path is a directory, not a file: {path}",
                    "content": ""
                }
            
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "size": len(content)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": ""
            }
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write or modify a file with new content
        
        Args:
            path: The file path to write
            content: The content to write to the file
            
        Returns:
            Dictionary with success status
        """
        try:
            # Normalize path and ensure it's within project root
            full_path = os.path.abspath(os.path.join(self.project_root, path))
            if not full_path.startswith(os.path.abspath(self.project_root)):
                return {
                    "success": False,
                    "error": "Access denied: Path is outside project directory"
                }
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "bytes_written": len(content.encode('utf-8'))
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_code(self, keyword: str) -> Dict[str, Any]:
        """
        Search for code patterns in the project
        
        Args:
            keyword: The keyword or pattern to search for
            
        Returns:
            Dictionary with success status and search results
        """
        try:
            results = []
            
            # Common code file extensions
            extensions = [
                '*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.java', '*.cpp', '*.c', '*.h',
                '*.hpp', '*.cs', '*.go', '*.rs', '*.php', '*.rb', '*.swift', '*.kt',
                '*.scala', '*.clj', '*.hs', '*.ml', '*.fs', '*.dart', '*.lua', '*.r',
                '*.m', '*.sh', '*.bat', '*.ps1', '*.sql', '*.html', '*.css', '*.scss',
                '*.less', '*.xml', '*.json', '*.yaml', '*.yml', '*.toml', '*.ini',
                '*.cfg', '*.conf', '*.md', '*.txt', '*.vue', '*.svelte'
            ]
            
            # Search through all code files
            for ext in extensions:
                pattern = os.path.join(self.project_root, '**', ext)
                for file_path in glob.glob(pattern, recursive=True):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                        
                        for line_num, line in enumerate(lines, 1):
                            if keyword.lower() in line.lower():
                                relative_path = os.path.relpath(file_path, self.project_root)
                                results.append({
                                    "file": relative_path,
                                    "line": line_num,
                                    "content": line.strip(),
                                    "context": self._get_context(lines, line_num - 1)
                                })
                                
                                # Limit results to prevent overwhelming output
                                if len(results) >= 50:
                                    break
                    
                    except Exception:
                        continue  # Skip files that can't be read
                    
                    if len(results) >= 50:
                        break
                
                if len(results) >= 50:
                    break
            
            return {
                "success": True,
                "results": results,
                "total_matches": len(results)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    def git_command(self, command: str) -> Dict[str, Any]:
        """
        Execute git commands safely
        
        Args:
            command: The git command to execute (without 'git' prefix)
            
        Returns:
            Dictionary with success status, stdout, stderr, and exit_code
        """
        # Safety check for dangerous git operations
        dangerous_git_commands = [
            'push --force', 'push -f', 'reset --hard', 'clean -fd', 'branch -D',
            'filter-branch', 'update-ref -d'
        ]
        
        full_command = f"git {command}"
        
        for dangerous in dangerous_git_commands:
            if dangerous in command:
                return {
                    "success": False,
                    "error": f"Dangerous git command blocked: {command}",
                    "stdout": "",
                    "stderr": "",
                    "exit_code": -1
                }
        
        # Special confirmation for push
        if command.startswith('push'):
            return {
                "success": False,
                "error": "Git push requires confirmation. Use 'git push' with explicit confirmation in the CLI.",
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        
        return self.run_shell(full_command)
    
    def detect_project_type(self) -> Dict[str, Any]:
        """
        Detect the project type based on configuration files
        
        Returns:
            Dictionary with project type information
        """
        project_files = []
        
        # Check for common project files
        checks = [
            ('package.json', 'node'),
            ('requirements.txt', 'python'),
            ('pyproject.toml', 'python'),
            ('Pipfile', 'python'),
            ('*.csproj', 'dotnet'),
            ('*.sln', 'dotnet'),
            ('pom.xml', 'java-maven'),
            ('build.gradle', 'java-gradle'),
            ('Cargo.toml', 'rust'),
            ('go.mod', 'go'),
            ('Makefile', 'make'),
            ('CMakeLists.txt', 'cmake'),
            ('composer.json', 'php'),
            ('Gemfile', 'ruby')
        ]
        
        for pattern, project_type in checks:
            if '*' in pattern:
                matches = glob.glob(os.path.join(self.project_root, pattern))
                if matches:
                    project_files.extend(matches)
                    return {
                        "success": True,
                        "type": project_type,
                        "files": matches
                    }
            else:
                file_path = os.path.join(self.project_root, pattern)
                if os.path.exists(file_path):
                    project_files.append(pattern)
                    return {
                        "success": True,
                        "type": project_type,
                        "files": [pattern]
                    }
        
        return {
            "success": True,
            "type": "unknown",
            "files": []
        }
    
    def get_build_command(self, project_type: str) -> str:
        """
        Get the appropriate build command for a project type
        
        Args:
            project_type: The detected project type
            
        Returns:
            Build command string
        """
        build_commands = {
            'node': 'npm run build',
            'python': 'python -m pytest || python -m unittest discover',
            'dotnet': 'dotnet build',
            'java-maven': 'mvn compile',
            'java-gradle': './gradlew build',
            'rust': 'cargo build',
            'go': 'go build',
            'make': 'make',
            'cmake': 'cmake --build .',
            'php': 'composer install',
            'ruby': 'bundle install'
        }
        
        return build_commands.get(project_type, 'echo "No build command defined for this project type"')
    
    def _is_dangerous_command(self, command: str) -> bool:
        """Check if a command is dangerous"""
        command_lower = command.lower()
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in command_lower:
                return True
        return False
    
    def _get_context(self, lines: List[str], line_index: int, context_lines: int = 3) -> List[str]:
        """Get context lines around a match"""
        start = max(0, line_index - context_lines)
        end = min(len(lines), line_index + context_lines + 1)
        
        context = []
        for i in range(start, end):
            prefix = ">>> " if i == line_index else "    "
            context.append(f"{prefix}{lines[i].rstrip()}")
        
        return context