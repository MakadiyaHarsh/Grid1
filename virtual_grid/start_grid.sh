#!/bin/bash

# Virtual Power Grid Simulator - Start Script
# This script starts the grid simulator with proper environment setup

echo "============================================================"
echo "⚡ VIRTUAL POWER GRID SIMULATOR - STARTUP"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Check if dependencies are installed
if [ ! -f "venv/bin/flask" ]; then
    echo "📦 Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
fi

echo "🚀 Starting Virtual Power Grid Simulator..."
echo ""
echo "Dashboard: http://localhost:5001"
echo "API Docs: See README.md"
echo ""
echo "Press Ctrl+C to stop the simulator"
echo "============================================================"
echo ""

# Start the simulator
./venv/bin/python3 grid_simulator.py
