# 🔐 Complete Command Reference Guide

## 📋 Table of Contents
1. [Starting the System](#starting-the-system)
2. [Sending Commands](#sending-commands)
3. [Viewing Output](#viewing-output)
4. [Monitoring Logs](#monitoring-logs)
5. [Testing Scenarios](#testing-scenarios)
6. [Stopping the System](#stopping-the-system)

---

## 🚀 Starting the System

### Step 1: Start Grid Simulator (Terminal 1)

```bash
# Navigate to grid simulator directory
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO WIBE/virtual_grid"

# Start the grid simulator
./venv/bin/python grid_simulator.py
```

**Expected Output:**
```
============================================================
⚡ VIRTUAL POWER GRID SIMULATOR
============================================================
Status: INITIALIZING
Grid State: OFFLINE
Listening on: http://localhost:5001
============================================================
```

---

### Step 2: Start Cybersecurity Gateway (Terminal 2)

```bash
# Navigate to gateway directory
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO WIBE/cyber_gateway"

# Start the gateway
./venv/bin/python gateway.py
```

**Expected Output:**
```
================================================================================
CYBERSECURITY GATEWAY FOR POWER GRID SYSTEM
================================================================================
Gateway Server: http://0.0.0.0:5002
Grid Simulator: http://localhost:5001
Risk Threshold: 0.7
================================================================================
[INFO] Gateway is OPERATIONAL and ready to receive commands
```

---

## 📤 Sending Commands

### Send Command via Terminal (Terminal 3)

**Basic Command Format:**
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```

### Example Commands

#### 1. Valid Normal Command
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```

#### 2. Turn Breaker OFF
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "OFF", "voltage": 0.95, "frequency": 50.0}'
```

#### 3. Adjust Voltage
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.05, "frequency": 50.0}'
```

#### 4. Adjust Frequency
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0, "frequency": 49.5}'
```

---

## 👁️ Viewing Output

### View Gateway Response (JSON Output)

The curl command will show the response immediately:

**Allowed Command Response:**
```json
{
  "status": "ALLOWED",
  "decision_layer": "Cybersecurity Gateway",
  "attack_type": "NORMAL",
  "risk_score": 0.1,
  "grid_response": {
    "status": "SUCCESS",
    "message": "Grid state updated",
    "grid_state": {
      "breaker": "ON",
      "voltage": 1.02,
      "frequency": 50.1,
      "power_flow": 102.0
    }
  },
  "request_id": "abc123",
  "timestamp": "2026-01-31T02:15:32.589175"
}
```

**Blocked Command Response:**
```json
{
  "status": "BLOCKED",
  "decision_layer": "Cybersecurity Gateway",
  "attack_type": "FDIA_SUSPECTED",
  "risk_score": 0.85,
  "reason": "Unrealistic high voltage-frequency combination",
  "details": "...",
  "request_id": "xyz789",
  "timestamp": "2026-01-31T02:15:45.932588"
}
```

### View Grid Telemetry Data

```bash
# Get current grid state
curl http://localhost:5001/grid/data
```

**Response:**
```json
{
  "breaker": "ON",
  "voltage": 1.02,
  "frequency": 50.1,
  "power_flow": 102.0,
  "last_update": 1769805932.590758
}
```

### Check System Health

```bash
# Check gateway health
curl http://localhost:5002/health
```

**Response:**
```json
{
  "gateway": "healthy",
  "grid_connection": "healthy",
  "timestamp": "2026-01-31T02:15:00.123456"
}
```

---

## 📊 Monitoring Logs

### Gateway Logs (Terminal 2)

Watch the gateway terminal for real-time security events:

```
[INFO] 2026-01-31 02:15:32 - [22b605cf] OPERATOR COMMAND RECEIVED
[INFO] 2026-01-31 02:15:32 - [22b605cf] Running cyber rules validation...
[INFO] 2026-01-31 02:15:32 - [22b605cf] CYBER RULES PASSED
[INFO] 2026-01-31 02:15:32 - [22b605cf] Running attack detection analysis...
[INFO] 2026-01-31 02:15:32 - [22b605cf] ATTACK DETECTION: NORMAL
[INFO] 2026-01-31 02:15:32 - [22b605cf] ANOMALY SCORE: 0.00
[INFO] 2026-01-31 02:15:32 - [22b605cf] COMBINED RISK SCORE: 0.10
[INFO] 2026-01-31 02:15:32 - [22b605cf] DECISION: ALLOWED
[INFO] 2026-01-31 02:15:32 - [22b605cf] FORWARDING TO GRID...
[INFO] 2026-01-31 02:15:32 - [22b605cf] GRID RESPONSE RECEIVED

================================================================================
CYBERSECURITY EVENT
================================================================================
Timestamp:      2026-01-31 02:15:32.591
Request ID:     22b605cf
Source:         Operator System
Command:        {'breaker': 'ON', 'voltage': 1.02, 'frequency': 50.1}
Decision:       ALLOWED
Attack Type:    NORMAL
Risk Score:     0.10
Grid Response:  {'status': 'SUCCESS', ...}
================================================================================
```

### Grid Simulator Logs (Terminal 1)

Watch the grid terminal for command execution:

```
[GRID] Command received from gateway
[GRID] Updating breaker state: ON
[GRID] Setting voltage: 1.02 pu
[GRID] Setting frequency: 50.1 Hz
[GRID] Calculating power flow: 102.0 MW
[GRID] State update successful
```

---

## 🧪 Testing Scenarios

### Run All Tests Automatically

```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO WIBE/cyber_gateway"
./demo.sh
```

This will run 8 test scenarios automatically.

---

### Manual Test Scenarios

#### Test 1: Normal Operation ✅
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```
**Expected:** ALLOWED, grid updated

---

#### Test 2: Voltage Violation 🚫
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.25, "frequency": 50.0}'
```
**Expected:** BLOCKED, voltage out of range

---

#### Test 3: Frequency Violation 🚫
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0, "frequency": 52.5}'
```
**Expected:** BLOCKED, frequency out of range

---

#### Test 4: FDIA Attack 🚫
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.10, "frequency": 51.0}'
```
**Expected:** BLOCKED, FDIA_SUSPECTED

---

#### Test 5: Missing Parameters 🚫
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0}'
```
**Expected:** BLOCKED, missing frequency

---

#### Test 6: Invalid Breaker State 🚫
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "INVALID", "voltage": 1.0, "frequency": 50.0}'
```
**Expected:** BLOCKED, invalid breaker state

---

#### Test 7: Replay Attack 🚫
```bash
# Send same command 5 times rapidly
for i in {1..5}; do
  curl -X POST http://localhost:5002/operator/command \
    -H "Content-Type: application/json" \
    -d '{"breaker": "ON", "voltage": 1.0, "frequency": 50.0}'
  sleep 0.5
done
```
**Expected:** First 2-3 ALLOWED, then BLOCKED (replay attack detected)

---

#### Test 8: Data Manipulation 🚫
```bash
# First send normal command
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 0.98, "frequency": 50.0}'

sleep 1

# Then send command with large spike
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.08, "frequency": 49.0}'
```
**Expected:** Second command may be flagged for data manipulation

---

## 🛑 Stopping the System

### Stop Gateway (Terminal 2)
Press `Ctrl + C` in the gateway terminal

### Stop Grid Simulator (Terminal 1)
Press `Ctrl + C` in the grid simulator terminal

---

## 📝 Quick Reference Card

### System URLs
- **Gateway API:** `http://localhost:5002/operator/command`
- **Grid Telemetry:** `http://localhost:5001/grid/data`
- **Gateway Health:** `http://localhost:5002/health`

### Valid Parameter Ranges
- **Voltage:** 0.90 - 1.10 pu
- **Frequency:** 49.0 - 51.0 Hz
- **Breaker:** "ON" or "OFF"

### Risk Threshold
- **Blocking Threshold:** 0.70
- Commands with risk > 0.70 are BLOCKED

### Command Template
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0, "frequency": 50.0}'
```

---

## 🔍 Troubleshooting Commands

### Check if Gateway is Running
```bash
curl http://localhost:5002/
```

### Check if Grid is Running
```bash
curl http://localhost:5001/
```

### Check Port Usage
```bash
# Check if port 5002 is in use
lsof -i :5002

# Check if port 5001 is in use
lsof -i :5001
```

### View Process List
```bash
ps aux | grep python
```

---

## 📚 Additional Resources

- **Full Documentation:** `README.md`
- **Quick Start Guide:** `QUICKSTART.md`
- **System Status:** `SYSTEM_STATUS.md`
- **Automated Demo:** `./demo.sh`

---

**⚡ GRID-SHIELD AI - Complete Command Reference**
