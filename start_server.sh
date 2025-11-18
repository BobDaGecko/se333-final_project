#!/bin/bash
#
# MCP Testing Agent - Startup Script
# Run this to start the MCP server quickly
#

set -e  # Exit on error

echo "============================================"
echo "MCP Testing Agent - Startup"
echo "============================================"
echo ""

# Check if we're in the right directory
if [ ! -f "mcp-server/server.py" ]; then
    echo "ERROR: Please run this script from the project root directory"
    echo "Expected path: Final_Project-SE333-Kellen_Siczka-11_16_25/"
    exit 1
fi

# Navigate to MCP server directory
cd mcp-server

echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "Found Python $PYTHON_VERSION"

if [ ! -d ".venv" ]; then
    echo ""
    echo "Virtual environment not found. Creating..."
    echo "This may take a minute..."
    uv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Checking dependencies..."
if ! python -c "import mcp" 2>/dev/null; then
    echo "Installing dependencies..."
    uv pip install -e .
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

echo ""
echo "============================================"
echo "Starting MCP Server..."
echo "============================================"
echo ""
echo "Server will run on: http://127.0.0.1:8000"
echo ""
echo "To connect in VS Code:"
echo "  1. Press Ctrl+Shift+P"
echo "  2. Type: MCP: Add Server"
echo "  3. Enter: http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "============================================"
echo ""

.venv/bin/python server.py
