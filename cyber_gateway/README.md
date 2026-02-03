# Cybersecurity Gateway for Power Grid System

## 🔐 Overview

The **Cybersecurity Gateway** is an industrial-grade security layer for the AI-Driven Cyber-Physical Power Grid Protection Platform. It acts as a mandatory security checkpoint between operator systems and the physical power grid, validating all commands, detecting cyber attacks, and enforcing security policies.

### System Architecture

```
Operator System
      ↓
Cybersecurity Gateway   ← THIS COMPONENT
      ↓
Virtual Power Grid Simulator
```

**Critical Design Principle:** The operator must NEVER communicate directly with the grid. All commands must pass through this gateway.

## 🎯 Key Features

- ✅ **Cyber Rules Engine** - Validates voltage, frequency, breaker states, and parameter integrity
- ✅ **Attack Detection** - Identifies FDIA, replay attacks, data manipulation, and correlation anomalies
- ✅ **Security Decision Engine** - Combines rule validation and attack detection for risk-based decisions
- ✅ **Grid Forwarding** - Safely forwards validated commands to the grid simulator
- ✅ **Security Event Logging** - Comprehensive, color-coded logging for audit and demonstration
- ✅ **REST API** - Flask-based API for operator command submission

## 📁 Project Structure

```
cyber_gateway/
│
├── gateway.py              # Main Flask server and security decision engine
├── config.py               # Configuration (grid connection, thresholds, rules)
├── rules_engine.py         # Cyber rule validation logic
├── attack_detector.py      # Attack detection algorithms
├── forwarder.py            # Grid communication module
├── logger.py               # Security event logging
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Virtual Power Grid Simulator running on port 5001

### Setup

1. **Navigate to the project directory:**
   ```bash
   cd cyber_gateway
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Edit `config.py` to customize gateway behavior:

```python
# Grid Simulator Connection
GRID_HOST = "localhost"
GRID_PORT = 6001

# Security Thresholds
RISK_THRESHOLD = 0.70  # Commands with risk > 0.70 will be blocked

# Cyber Rule Boundaries
VOLTAGE_MIN = 0.90  # per unit
VOLTAGE_MAX = 1.10  # per unit
FREQUENCY_MIN = 49.0  # Hz
FREQUENCY_MAX = 51.0  # Hz
```

## 🏃 Running the Gateway

1. **Ensure the Virtual Power Grid Simulator is running:**
   ```bash
   # In another terminal, start the grid simulator
   cd ../virtual_grid
   python grid_simulator.py
   ```

2. **Start the Cybersecurity Gateway:**
   ```bash
   python gateway.py
   ```

3. **Expected output:**
   ```
   ================================================================================
   CYBERSECURITY GATEWAY FOR POWER GRID SYSTEM
   ================================================================================
   Gateway Server: http://0.0.0.0:5002
   Grid Simulator: http://localhost:5001
   Risk Threshold: 0.70
   ================================================================================
   
   [INFO] 2026-01-31 02:00:00 - Cybersecurity Gateway starting...
   [INFO] 2026-01-31 02:00:00 - Operator endpoint: POST /operator/command
   [INFO] 2026-01-31 02:00:00 - Grid simulator connection: HEALTHY
   [INFO] 2026-01-31 02:00:00 - Gateway is OPERATIONAL and ready to receive commands
   ```

## 📡 API Documentation

### POST /operator/command

Submit operator commands for security validation and grid forwarding.

**Endpoint:** `http://localhost:5002/operator/command`

**Request Format:**
```json
{
  "breaker": "ON",
  "voltage": 1.02,
  "frequency": 50.1
}
```

**Response Format (Allowed):**
```json
{
  "status": "ALLOWED",
  "decision_layer": "Cybersecurity Gateway",
  "attack_type": "NORMAL",
  "risk_score": 0.12,
  "grid_response": {
    "status": "success",
    "message": "Command executed",
    "telemetry": { ... }
  },
  "request_id": "a3f2c1d8",
  "timestamp": "2026-01-31T02:00:00.123456"
}
```

**Response Format (Blocked):**
```json
{
  "status": "BLOCKED",
  "decision_layer": "Cybersecurity Gateway",
  "attack_type": "FDIA_SUSPECTED",
  "risk_score": 0.87,
  "reason": "Both voltage and frequency at extreme boundaries - FDIA pattern",
  "details": "Both voltage and frequency at extreme boundaries - FDIA pattern",
  "request_id": "b7e4d2c9",
  "timestamp": "2026-01-31T02:00:01.234567"
}
```

### GET /health

Check gateway and grid connection health.

**Response:**
```json
{
  "gateway": "healthy",
  "grid_connection": "healthy",
  "timestamp": "2026-01-31T02:00:00.123456"
}
```

## 🛡️ Security Features

### Cyber Rules Engine

Validates commands against industrial power grid safety rules:

| Rule | Validation | Risk Level |
|------|------------|------------|
| **Missing Parameters** | Checks for breaker, voltage, frequency | 0.90 |
| **Voltage Range** | Must be 0.90 - 1.10 pu | 0.80 |
| **Frequency Range** | Must be 49.0 - 51.0 Hz | 0.80 |
| **Breaker State** | Must be "ON" or "OFF" | 0.70 |
| **Data Types** | Validates numeric and string types | 0.85 |

### Attack Detection Algorithms

#### 1. False Data Injection Attack (FDIA)
- Detects parameters at extreme boundaries
- Identifies unrealistic parameter combinations
- Risk Score: 0.65 - 0.85

#### 2. Data Manipulation
- Tracks abnormal value spikes
- Detects sudden parameter changes
- Risk Score: 0.70 - 0.80

#### 3. Replay Attack
- Monitors rapid command repetition
- Detects identical commands within time window
- Risk Score: 0.60 - 0.90

#### 4. Parameter Correlation Anomalies
- Validates voltage-frequency relationships
- Detects inconsistent breaker-parameter states
- Risk Score: 0.55 - 0.65

### Security Decision Logic

```python
combined_risk = max(rules_risk, attack_anomaly_score)

if combined_risk > RISK_THRESHOLD or rules_violated:
    BLOCK command
else:
    FORWARD to grid
```

## 🧪 Testing & Demonstration

### Test 1: Normal Operation

```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```

**Expected:** ✅ ALLOWED, forwarded to grid, low risk score

### Test 2: Voltage Violation

```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.25, "frequency": 50.0}'
```

**Expected:** 🚫 BLOCKED, voltage out of range

### Test 3: FDIA Detection

```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.10, "frequency": 51.0}'
```

**Expected:** 🚫 BLOCKED or high risk, FDIA_SUSPECTED

### Test 4: Replay Attack

```bash
# Send same command 5 times rapidly
for i in {1..5}; do
  curl -X POST http://localhost:5002/operator/command \
    -H "Content-Type: application/json" \
    -d '{"breaker": "ON", "voltage": 1.0, "frequency": 50.0}'
  sleep 0.5
done
```

**Expected:** 🚫 REPLAY_ATTACK detected

### Test 5: Missing Parameters

```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0}'
```

**Expected:** 🚫 BLOCKED, missing frequency parameter

## 📊 Security Event Logs

All events are logged with structured format:

```
================================================================================
CYBERSECURITY EVENT
================================================================================
Timestamp:      2026-01-31 02:00:00.123
Request ID:     a3f2c1d8
Source:         Operator System
Command:        {'breaker': 'ON', 'voltage': 1.02, 'frequency': 50.1}
Decision:       ALLOWED
Attack Type:    NORMAL
Risk Score:     0.12
Grid Response:  {'status': 'success', ...}
================================================================================
```

## 🔬 Technical Details

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **gateway.py** | Main server, request handling, security decision flow |
| **rules_engine.py** | Parameter validation, cyber rule enforcement |
| **attack_detector.py** | Attack pattern recognition, anomaly scoring |
| **forwarder.py** | HTTP communication with grid simulator |
| **logger.py** | Structured logging, color-coded output |
| **config.py** | Centralized configuration management |

### Design Principles

1. **Separation of Concerns** - Each module has a single, well-defined responsibility
2. **Defense in Depth** - Multiple security layers (rules + attack detection)
3. **Fail-Safe** - Blocks commands when in doubt
4. **Auditability** - Complete logging of all security decisions
5. **Modularity** - Easy to extend with AI models in future phases

## 🚀 Future Integration

This gateway is designed to support future enhancements:

- **AI Anomaly Models** - Machine learning-based attack detection
- **Cyber-Physical Correlation** - Cross-layer security analysis
- **Reinforcement Learning** - Adaptive security policies
- **Automated Response** - Dynamic threat mitigation

## 📚 Use Cases

This system is suitable for:

- ✅ Academic research and publications
- ✅ SSIP (Student Startup and Innovation Policy) evaluation
- ✅ Patent documentation
- ✅ Technical presentations and demonstrations
- ✅ Industrial SCADA security training

## 🔧 Troubleshooting

### Gateway can't connect to grid simulator

**Error:** `Cannot connect to grid at http://localhost:6001`

**Solution:**
1. Verify grid simulator is running: `curl http://localhost:6001`
2. Check port configuration in `config.py`
3. Ensure no firewall blocking port 6001

### Commands always blocked

**Issue:** All commands showing high risk scores

**Solution:**
1. Check `RISK_THRESHOLD` in `config.py` (default: 0.70)
2. Verify command parameters are within valid ranges
3. Review attack detector sensitivity settings

## 📄 License

This project is part of the AI-Driven Cyber-Physical Power Grid Protection Platform.

## 👥 Authors

Developed for academic research and industrial cybersecurity demonstration.

---

**⚡ GRID-SHIELD AI - Protecting Critical Infrastructure**
