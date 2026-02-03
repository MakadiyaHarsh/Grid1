#!/bin/bash
cd "$(dirname "$0")/cyber_gateway"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================="
echo "🛡️  CYBERSECURITY GATEWAY"
echo "=========================================="
echo ""

# Run gateway
python3 gateway.py

# If it exits, show error and wait
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "ERROR: Gateway exited with code $EXIT_CODE"
fi
echo ""
echo "Press Enter to close this window..."
read
