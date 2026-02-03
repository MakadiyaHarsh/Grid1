#!/bin/bash
cd "$(dirname "$0")"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================="
echo "⚠️  ATTACK SIMULATOR"
echo "=========================================="
echo ""

# Run attack simulator
python3 attack_simulator.py

# Wait before closing
echo ""
echo "Press Enter to close this window..."
read
