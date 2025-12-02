#!/bin/bash
#
# Launch Urban Heat Island Web Dashboard
# Usage: bash run_dashboard.sh
#

echo "================================================"
echo "Urban Heat Island Dashboard"
echo "================================================"
echo ""

# Navigate to the dashboard directory
cd "$(dirname "$0")/../web_dashboard" || exit 1

echo "Starting web server..."
echo ""
echo "Dashboard will open in your browser at:"
echo "  → http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================"
echo ""

# Run the Python server
python3 server.py

