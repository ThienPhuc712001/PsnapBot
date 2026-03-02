"""
Main entry point for PSnapBOT - Local Persistent Development Agent
Provides CLI interface and argument parsing
"""
import argparse
import sys
import os
from agent.core import DevAgent


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="PSnapBOT - Local Persistent Development Agent - AI-powered development assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Start interactive mode
  python main.py --help                   # Show help
  python main.py --version                # Show version
  python main.py --status                 # Show agent status
  python main.py "fix build"              # Process single command
  python main.py --project /path/to/project "add feature"
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to execute (optional, starts interactive mode if not provided)"
    )
    
    parser.add_argument(
        "--project", "-p",
        help="Path to the project directory (default: current directory)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="PSnapBOT v1.0.0"
    )
    
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show agent status and exit"
    )
    
    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="Show agent information and exit"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress non-essential output"
    )
    
    args = parser.parse_args()
    
    # Change to project directory if specified
    if args.project:
        if not os.path.exists(args.project):
            print(f"Error: Project directory '{args.project}' does not exist.")
            sys.exit(1)
        
        try:
            os.chdir(args.project)
            if not args.quiet:
                print(f"Changed to project directory: {os.getcwd()}")
        except Exception as e:
            print(f"Error: Could not change to directory '{args.project}': {str(e)}")
            sys.exit(1)
    
    # Initialize the agent
    try:
        agent = DevAgent()
    except Exception as e:
        print(f"Error: Failed to initialize agent: {str(e)}")
        sys.exit(1)
    
    # Handle different modes
    if args.status:
        agent._show_status()
        return
    
    if args.info:
        info = agent.get_agent_info()
        print(f"""
{info['name']} v{info['version']}
=====================================

Components:
""")
        for component, description in info['components'].items():
            print(f"  • {component}: {description}")
        
        print(f"\nCapabilities:")
        for capability in info['capabilities']:
            print(f"  • {capability}")
        
        print(f"\nSafety Features:")
        for feature in info['safety_features']:
            print(f"  • {feature}")
        
        return
    
    # Process single command or start interactive mode
    if args.command:
        # Process single command
        if not args.quiet:
            print(f"Processing command: {args.command}")
        
        try:
            result = agent.process_request(args.command)
            
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                sys.exit(1)
            
            # Show additional details if available
            if "details" in result and not args.quiet:
                print("\nDetails:")
                for key, value in result["details"].items():
                    if isinstance(value, list):
                        print(f"  {key}:")
                        for item in value:
                            print(f"    - {item}")
                    else:
                        print(f"  {key}: {value}")
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    
    else:
        # Start interactive mode
        try:
            agent.interactive_mode()
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()