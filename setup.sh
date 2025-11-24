#!/bin/bash
# Setup script for AVM MCP Server with multi-transport support

echo "=========================================="
echo "AVM MCP Server - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Test import
echo "🧪 Testing imports..."
python3 -c "
import logging
import requests
print('✅ Basic imports successful')
try:
    from mcp.server.fastmcp import FastMCP
    print('✅ FastMCP import successful')
except ImportError as e:
    print(f'⚠️  FastMCP import issue: {e}')
    print('   This is expected if fastmcp is not properly installed')
"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the server:"
echo "  STDIO mode (default):  python server.py"
echo "  HTTP mode:             python server.py --transport http"
echo "  SSE mode:              python server.py --transport sse"
echo "  With debug:            python server.py --transport http --debug"
echo ""
echo "To test HTTP transport:"
echo "  python test_transports.py"
echo ""
