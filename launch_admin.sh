#!/bin/bash
cd "$(dirname "$0")"

# Activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run admin console
python3 admin_console.py

# Wait before closing
echo ""
echo "Press Enter to close this window..."
read
