#!/bin/bash
# Quick Command Cheat Sheet for GRID-SHIELD AI

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         GRID-SHIELD AI - Quick Command Cheat Sheet            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "📍 SYSTEM URLS:"
echo "   Gateway:  http://localhost:5002/operator/command"
echo "   Grid:     http://localhost:5001/grid/data"
echo "   Health:   http://localhost:5002/health"
echo ""

echo "🚀 START SYSTEM:"
echo "   Terminal 1: cd virtual_grid && ./venv/bin/python grid_simulator.py"
echo "   Terminal 2: cd cyber_gateway && ./venv/bin/python gateway.py"
echo ""

echo "📤 SEND VALID COMMAND:"
echo "   curl -X POST http://localhost:5002/operator/command \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"breaker\": \"ON\", \"voltage\": 1.02, \"frequency\": 50.1}'"
echo ""

echo "🚫 TEST ATTACK (FDIA):"
echo "   curl -X POST http://localhost:5002/operator/command \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"breaker\": \"ON\", \"voltage\": 1.10, \"frequency\": 51.0}'"
echo ""

echo "👁️  VIEW GRID STATE:"
echo "   curl http://localhost:5001/grid/data"
echo ""

echo "🧪 RUN ALL TESTS:"
echo "   cd cyber_gateway && ./demo.sh"
echo ""

echo "📊 VALID RANGES:"
echo "   Voltage:    0.90 - 1.10 pu"
echo "   Frequency:  49.0 - 51.0 Hz"
echo "   Breaker:    ON or OFF"
echo "   Risk Limit: 0.70 (commands > 0.70 blocked)"
echo ""

echo "🛑 STOP SYSTEM:"
echo "   Press Ctrl+C in both terminals"
echo ""

echo "📚 DOCUMENTATION:"
echo "   Full Guide:    COMMANDS.md"
echo "   Quick Start:   QUICKSTART.md"
echo "   System Status: SYSTEM_STATUS.md"
echo ""
