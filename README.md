# PSnapBOT - Local Persistent Development Agent

PSnapBOT is a lightweight, autonomous development assistant that runs on your personal PC and helps you develop multi-language software projects.

## Features

- 🧠 **Intelligent**: Uses GLM-4.6 via AgentRouter for smart decision making
- 💾 **Persistent Memory**: Stores interactions and fixes locally in SQLite
- 🔧 **Build-Fix Loop**: Automatically detects and fixes build errors
- 🛡️ **Safe Execution**: Restricted shell commands with safety checks
- 📁 **Multi-Language**: Supports Python, JavaScript, Java, C#, Rust, Go, and more
- 🚀 **Lightweight**: No heavy frameworks, minimal dependencies
- 💰 **Free**: Only costs existing model usage, no external services

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the agent:**
   ```bash
   python main.py
   ```

3. **Use in interactive mode:**
   ```
   > fix build
   > add login feature
   > explain project structure
   > search for user authentication
   ```

## 📁 Project Structure

```
dev_agent/
│
├── agent/
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Main agent loop and coordination
│   ├── planner.py           # Request analysis and action planning
│   ├── executor.py          # Tool execution and build-fix loop
│   ├── memory.py            # SQLite database operations
│   ├── llm.py               # GLM-4.6 API integration
│   └── tools.py             # Shell, file, and git operations
│
├── data/
│   └── memory.db            # SQLite database (created automatically)
│
├── config.py                # Configuration settings
├── main.py                  # CLI interface and entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 💻 Usage

### 🎯 Interactive Mode

Start the agent and interact naturally:

```bash
python main.py
```

Available commands in interactive mode:
- `help` - Show help information
- `status` - Show agent status and statistics
- `history` - Show recent conversation history
- `clear` - Clear conversation history
- `exit` - Exit the agent

### ⚡ Single Command Mode

Execute a single command and exit:

```bash
python main.py "fix build"
python main.py "add user authentication"
python main.py --project /path/to/project "explain code"
```

### ⚙️ Command Line Options

- `--project, -p` - Specify project directory (default: current)
- `--status, -s` - Show agent status and exit
- `--info, -i` - Show agent information and exit
- `--quiet, -q` - Suppress non-essential output
- `--version, -v` - Show version information

## 🎯 Capabilities

### 🔧 Build Error Fixing

The agent automatically:
1. Detects project type (Node.js, Python, .NET, Java, etc.)
2. Runs appropriate build command
3. Analyzes build errors
4. Searches for similar past fixes
5. Applies targeted fixes
6. Verifies the fix works
7. Saves successful fixes to memory

### ✨ Feature Development

- Analyze requirements
- Search existing code
- Design implementation
- Write new code
- Test implementation
- Document changes

### 🔍 Code Analysis

- Explain project structure
- Analyze code patterns
- Review code quality
- Identify improvements

### 🔄 Refactoring

- Identify refactoring opportunities
- Plan refactoring approach
- Apply changes safely
- Test refactored code

### 📚 Git Operations

Safe git operations with confirmation:
- `git status`, `git add`, `git commit`
- `git branch`, `git checkout`, `git merge`
- `git pull` (with confirmation for `git push`)

### 🔎 Code Search

- Search through all code files
- Find functions, classes, variables
- Locate specific patterns
- Get context around matches

## 🛡️ Safety Features

- **Restricted Shell**: Only allows safe, development-related commands
- **Project Confinement**: All operations limited to project directory
- **Dangerous Command Blocking**: Prevents destructive commands
- **Git Push Confirmation**: Requires confirmation before pushing changes
- **Memory-Based Learning**: Learns from past fixes without external services

## 🌐 Supported Project Types

- **Node.js**: `package.json` → `npm run build`
- **Python**: `requirements.txt`, `pyproject.toml` → `python -m pytest`
- **.NET**: `*.csproj`, `*.sln` → `dotnet build`
- **Java (Maven)**: `pom.xml` → `mvn compile`
- **Java (Gradle)**: `build.gradle` → `./gradlew build`
- **Rust**: `Cargo.toml` → `cargo build`
- **Go**: `go.mod` → `go build`
- **Make**: `Makefile` → `make`
- **CMake**: `CMakeLists.txt` → `cmake --build .`
- **PHP**: `composer.json` → `composer install`
- **Ruby**: `Gemfile` → `bundle install`

## 💾 Memory System

The agent stores three types of information:

1. **Sessions**: Every user interaction and agent response
2. **Build History**: Build errors and successful fixes
3. **Project Knowledge**: Key information about the project

All data is stored locally in SQLite at `data/memory.db`.

## ⚙️ Configuration

Edit `config.py` to customize:

- API settings (timeout, retries)
- Safety rules and allowed commands
- Database paths
- Performance constraints

## 📋 Requirements

- Python 3.10+
- Internet connection (for GLM-4.6 API)
- No GPU required
- No external dependencies beyond `requests`

## 💡 Examples

### 🛠️ Fix Build Errors
```
> fix build
✅ Build fixed successfully after 2 attempts!
Details:
  attempts: 2
  fixes_applied:
    - Fixed missing import in user_service.py
    - Updated dependency version in package.json
```

### ➕ Add Features
```
> add user login feature
✅ Implemented user login feature with JWT authentication
Details:
  files_created:
    - auth/login.py
    - auth/jwt_utils.py
    - tests/test_login.py
```

### 📊 Analyze Code
```
> explain project structure
✅ This is a Flask web application with the following structure:
  - app/: Main application code
  - auth/: Authentication modules
  - api/: REST API endpoints
  - tests/: Unit and integration tests
```

## 🔧 Troubleshooting

### ⚠️ Common Issues

1. **API Connection Error**: Check internet connection and API availability
2. **Permission Denied**: Ensure the agent has read/write access to the project directory
3. **Database Locked**: Close other instances of the agent
4. **Command Not Found**: Ensure the required build tools are installed

### 🐛 Debug Mode

Set `LOG_LEVEL = "DEBUG"` in `config.py` for detailed logging.

## 🤝 Contributing

This is a standalone agent designed for personal use. Feel free to modify the code to suit your specific needs.

## 📄 License

This project is provided as-is for educational and personal use.