#!/bin/bash
# Quick launcher for Interactive UI

echo "🎨 Launching GRID-SHIELD AI Interactive Terminal UI..."
echo ""

# Check if gateway is running
if ! curl -s http://localhost:5002/health > /dev/null 2>&1; then
    echo "⚠️  WARNING: Gateway is not running on port 5002"
    echo "   Start it with: ./venv/bin/python gateway.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Launch the UI
./venv/bin/python interactive_ui.py
