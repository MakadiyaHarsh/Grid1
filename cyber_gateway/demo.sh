#!/bin/bash

# Cybersecurity Gateway Demonstration Script
# This script demonstrates various security scenarios

echo "=========================================="
echo "CYBERSECURITY GATEWAY DEMONSTRATION"
echo "=========================================="
echo ""

GATEWAY_URL="http://localhost:5002/operator/command"

echo "Test 1: Normal Operation (Valid Command)"
echo "------------------------------------------"
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
echo -e "\n"
sleep 1

echo "Test 2: Voltage Violation"
echo "------------------------------------------"
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.25, "frequency": 50.0}'
echo -e "\n"
sleep 1

echo "Test 3: Frequency Violation"
echo "------------------------------------------"
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0, "frequency": 52.5}'
echo -e "\n"
sleep 1

echo "Test 4: FDIA Detection (Extreme Boundaries)"
echo "------------------------------------------"
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.10, "frequency": 51.0}'
echo -e "\n"
sleep 1

echo "Test 5: Missing Parameters"
echo "------------------------------------------"
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0}'
echo -e "\n"
sleep 1

echo "Test 6: Invalid Breaker State"
echo "------------------------------------------"
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "INVALID", "voltage": 1.0, "frequency": 50.0}'
echo -e "\n"
sleep 1

echo "Test 7: Replay Attack Detection"
echo "------------------------------------------"
echo "Sending identical command 5 times rapidly..."
for i in {1..5}; do
  curl -X POST $GATEWAY_URL \
    -H "Content-Type: application/json" \
    -d '{"breaker": "ON", "voltage": 0.95, "frequency": 49.8}'
  echo ""
  sleep 0.5
done
echo -e "\n"

echo "Test 8: Data Manipulation (Large Spike)"
echo "------------------------------------------"
# First send a normal command
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 0.98, "frequency": 50.0}'
echo -e "\n"
sleep 0.5

# Then send a command with large spike
curl -X POST $GATEWAY_URL \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.08, "frequency": 49.0}'
echo -e "\n"
sleep 1

echo "=========================================="
echo "DEMONSTRATION COMPLETE"
echo "=========================================="
echo ""
echo "Check the gateway terminal for detailed security logs!"
