"""
Configuration for PSnapBOT - Local Persistent Development Agent
"""
import os

# API Configuration
API_BASE_URL = "https://agentrouter.org/v1/chat/completions"
API_MODEL = "glm-4.6"
API_TIMEOUT = 30
API_MAX_RETRIES = 3

# Project Configuration
PROJECT_ROOT = os.getcwd()
SHELL_TIMEOUT = 60
MAX_BUILD_ATTEMPTS = 5

# Database Configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "data", "memory.db")

# Safety Configuration
ALLOWED_SHELL_COMMANDS = [
    "git", "npm", "node", "python", "pip", "dotnet", "mvn", "gradle", "make", "cmake",
    "gcc", "g++", "clang", "clang++", "javac", "java", "go", "cargo", "rustc"
]

DANGEROUS_COMMANDS = [
    "rm -rf", "del /s", "format", "fdisk", "mkfs", "shutdown", "reboot",
    "sudo rm", "sudo del", "chmod 777", "chown", "passwd"
]

# Logging Configuration
LOG_LEVEL = "INFO"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB

# Memory Configuration
MAX_CONTEXT_LENGTH = 8000
SIMILARITY_THRESHOLD = 0.7