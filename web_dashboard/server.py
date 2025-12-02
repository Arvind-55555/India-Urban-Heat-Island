#!/usr/bin/env python3
"""
Simple HTTP Server for Urban Heat Island Dashboard
Run this script to view the dashboard in your web browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration
PORT = 8000
HOST = 'localhost'

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files correctly"""
    
    def end_headers(self):
        # Enable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def main():
    # Change to the web_dashboard directory
    dashboard_dir = Path(__file__).parent
    os.chdir(dashboard_dir)
    
    print("=" * 80)
    print(" Urban Heat Island Dashboard - Web Server")
    print("=" * 80)
    print(f"\nStarting server on http://{HOST}:{PORT}")
    print(f"Dashboard directory: {dashboard_dir}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80 + "\n")
    
    # Create server
    with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
        # Open browser automatically
        url = f"http://{HOST}:{PORT}"
        print(f"Opening browser at {url}...")
        webbrowser.open(url)
        
        try:
            print(f"\n✓ Server running at {url}")
            print("✓ Dashboard is now accessible in your web browser")
            print("\nServing requests...\n")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("Server stopped by user")
            print("=" * 80)
            sys.exit(0)

if __name__ == "__main__":
    main()

