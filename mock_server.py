#!/usr/bin/env python3
"""
Mock API server for testing PSnapBOT
"""
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Mock response for chat completions
            response = {
                "id": "chatcmpl-mock",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": data.get("model", "glm-4.6"),
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"Mock response for: {data.get('messages', [{}])[-1].get('content', 'hello')}"
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 10,
                    "total_tokens": 20
                }
            }
            
            self.send_response(200, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }, json.dumps(response))
            
        except Exception as e:
            error_response = {
                "error": {
                    "message": f"Mock server error: {str(e)}",
                    "type": "mock_error"
                }
            }
            self.send_response(500, {'Content-Type': 'application/json'}, json.dumps(error_response))
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200, {'Content-Type': 'application/json'}, json.dumps({"status": "ok", "service": "mock-api"}))
        else:
            self.send_response(404, {'Content-Type': 'text/plain'}, 'Not Found')
    
    def send_response(self, code, headers, body):
        self.send_response_only(code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

def run_server():
    server_address = ('127.0.0.1', 6969)
    httpd = HTTPServer(server_address, MockAPIHandler)
    
    print("🚀 Mock API Server Starting...")
    print(f"📍 Address: http://{server_address[0]}:{server_address[1]}")
    print("🔄 Ready to test PSnapBOT!")
    print("📝 Mock responses will be sent")
    print("⚠ Press Ctrl+C to stop server")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()