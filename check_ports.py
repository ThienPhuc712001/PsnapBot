#!/usr/bin/env python3
"""
Check common AgentRouterAnywhere ports
"""
import socket
import sys

def check_port(host, port):
    """Check if port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            return True
        else:
            return False
    except:
        return False

def main():
    host = "127.0.0.1"
    
    # Common AgentRouterAnywhere ports
    ports = [6969, 6970, 6971, 6972, 8080, 8000, 3000, 5000]
    
    print("Checking AgentRouterAnywhere ports...")
    print(f"Host: {host}")
    print()
    
    for port in ports:
        if check_port(host, port):
            print(f"✓ Port {port}: OPEN (AgentRouterAnywhere detected)")
        else:
            print(f"✗ Port {port}: Closed")
    
    print()
    print("If no ports are open:")
    print("1. Make sure AgentRouterAnywhere is running")
    print("2. Check the port in AgentRouterAnywhere settings")
    print("3. Update the port in config files")
    print()
    print("Common AgentRouterAnywhere ports:")
    print("- 6969 (default)")
    print("- 6970-6972 (alternative)")
    print("- 8080, 8000 (web interface)")

if __name__ == "__main__":
    main()