#!/bin/bash
cd "$(dirname "$0")/virtual_grid"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================="
echo "⚡ VIRTUAL POWER GRID SIMULATOR"
echo "=========================================="
echo ""

# Run grid simulator
python3 grid_simulator.py

# If it exits, show error and wait
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "ERROR: Grid simulator exited with code $EXIT_CODE"
fi
echo ""
echo "Press Enter to close this window..."
read
