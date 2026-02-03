# Virtual Power Grid Simulator

A realistic electrical grid control system simulator designed for cybersecurity and AI research demonstrations.

## 🔷 Overview

This component represents the **Physical Power Grid + Substation Execution Layer** in a cyber-physical security architecture. It simulates realistic grid behavior, processes control commands, and generates real-time telemetry.

### Architecture

```
Operator System
      ↓
Cybersecurity Gateway  (Laptop-2)
      ↓
Virtual Power Grid     (Laptop-3) ← This Component
```

## 🔷 Key Features

✅ **Realistic Grid State Model**
- Voltage (per-unit: 0.90 - 1.10)
- Frequency (Hz: 49.0 - 51.0)
- Breaker state (ON/OFF)
- Power flow (MW, derived)
- Timestamp tracking

✅ **Realistic Power System Behavior**
- Breaker OFF: voltage=0, frequency=0, power_flow=0
- Breaker ON: commanded values applied, power calculated

✅ **Real-Time Telemetry**
- Auto-updating every 1 second
- Continuous monitoring support
- JSON-based data format

✅ **Security Architecture**
- Direct operator access **BLOCKED**
- Gateway-only control access
- Read-only telemetry endpoints

✅ **Event Logging**
- Command execution logs
- State change logs
- Security violation logs

✅ **Modern Dashboard**
- Real-time SCADA-style interface
- Auto-refresh display
- Color-coded status indicators

## 🔷 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/harsh/Documents/GRID-SHIELD\ AI/DEMO\ WIBE/virtual_grid
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the simulator:**
   ```bash
   python3 grid_simulator.py
   ```

4. **Access the dashboard:**
   Open your browser to: `http://localhost:5001`

## 🔷 API Endpoints

### 1. Gateway Control Command
**Endpoint:** `POST /grid/command`

**Description:** Accepts control commands from the cybersecurity gateway.

**Request Body:**
```json
{
  "breaker": "ON",
  "voltage": 1.02,
  "frequency": 50.1
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "message": "Grid state updated",
  "grid_state": {
    "voltage": 1.02,
    "frequency": 50.1,
    "breaker": "ON",
    "power_flow": 102.0,
    "last_update": 1738267559.123
  }
}
```

**Validation Rules:**
- `breaker`: Must be "ON" or "OFF"
- `voltage`: Must be 0.90 - 1.10 pu
- `frequency`: Must be 49.0 - 51.0 Hz

---

### 2. Read-Only Telemetry
**Endpoint:** `GET /grid/data`

**Description:** Returns current grid telemetry (read-only).

**Response:**
```json
{
  "status": "SUCCESS",
  "grid_state": {
    "voltage": 1.02,
    "frequency": 50.1,
    "breaker": "ON",
    "power_flow": 102.0,
    "last_update": 1738267559.123
  },
  "timestamp": "2026-01-31T01:45:59.123456"
}
```

---

### 3. Operator Access Block (Security)
**Endpoint:** `POST /operator/command`

**Description:** **ALWAYS DENIES** direct operator access.

**Response:**
```json
{
  "status": "DENIED",
  "reason": "Direct operator access not allowed"
}
```

**HTTP Status:** `403 Forbidden`

---

### 4. Dashboard
**Endpoint:** `GET /`

**Description:** Serves the real-time SCADA monitoring dashboard.

## 🔷 Usage Examples

### Example 1: Turn Breaker ON (via Gateway)

```bash
curl -X POST http://localhost:5001/grid/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.00, "frequency": 50.0}'
```

**Expected Output:**
```
⚡ GRID EVENT - COMMAND_RECEIVED
Timestamp: 2026-01-31 01:45:59
------------------------------------------------------------
Source: Cybersecurity Gateway
Breaker: ON
Voltage: 1.00 pu
Frequency: 50.0 Hz
Power Flow: 100.00 MW
============================================================
```

---

### Example 2: Query Telemetry

```bash
curl http://localhost:5001/grid/data
```

---

### Example 3: Attempt Direct Operator Access (Blocked)

```bash
curl -X POST http://localhost:5001/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.00, "frequency": 50.0}'
```

**Expected Output:**
```
⚡ GRID EVENT - SECURITY_VIOLATION
Timestamp: 2026-01-31 01:46:00
------------------------------------------------------------
Attempt: Direct operator access
Endpoint: /operator/command
Status: DENIED
Reason: Direct operator access not allowed
============================================================
```

---

### Example 4: Invalid Command (Validation Error)

```bash
curl -X POST http://localhost:5001/grid/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.50, "frequency": 50.0}'
```

**Response:**
```json
{
  "status": "ERROR",
  "message": "Voltage out of range. Must be 0.90-1.10 pu (received: 1.5)"
}
```

## 🔷 Security Model

### Design Principle

This grid simulator follows the **defense-in-depth** principle:

1. **Physical Layer** (This Component): Pure grid behavior, no intelligence
2. **Security Layer** (Gateway): Authentication, authorization, anomaly detection
3. **AI Layer** (Future): Predictive threat detection, automated response

### Why Direct Operator Access is Blocked

In real industrial control systems:
- Operators should **never** have direct access to physical equipment
- All commands must flow through **authenticated and authorized** gateways
- This prevents:
  - Unauthorized access
  - Insider threats
  - Cyber attacks bypassing security controls

### Demonstration Scenarios

| Scenario | Flow | Result |
|----------|------|--------|
| **Normal Operation** | Operator → Gateway → Grid | ✅ Command executed |
| **Direct Attack** | Operator → Grid | ❌ Access denied |
| **Cyber Attack** | Attacker → Gateway → Grid | ⚠️ Gateway decides (future AI integration) |

## 🔷 Grid Behavior Logic

### Breaker OFF State
```
voltage      = 0.0
frequency    = 0.0
power_flow   = 0.0
```

### Breaker ON State
```
voltage      = commanded value (0.90 - 1.10 pu)
frequency    = commanded value (49.0 - 51.0 Hz)
power_flow   = voltage × 100.0 MW
```

### Power Flow Calculation
Simplified model:
```
P = V × I_factor
where I_factor = 100.0 (constant)
```

> **Note:** This is a simplified electrical model for demonstration purposes. Real power flow analysis involves complex AC power calculations, impedance networks, and load flow algorithms.

## 🔷 Dashboard Features

### Real-Time Display
- **Voltage**: Color-coded (green=normal, yellow=warning, red=critical)
- **Frequency**: Color-coded status indicators
- **Breaker**: Visual ON/OFF indicator with pulse animation
- **Power Flow**: Real-time MW calculation

### Status Indicators
- 🟢 **NORMAL**: Values within optimal range
- 🟡 **WARNING**: Values within acceptable but non-optimal range
- 🔴 **CRITICAL**: Values outside acceptable range
- ⚫ **OFFLINE**: Breaker OFF, no power flow

### Auto-Refresh
- Fetches telemetry every **1 second**
- Connection status indicator
- Automatic reconnection on network recovery

## 🔷 Event Logging

All grid events are logged to the terminal in a structured format:

```
============================================================
⚡ GRID EVENT - [EVENT_TYPE]
Timestamp: [ISO-8601 timestamp]
------------------------------------------------------------
[Event Details]
============================================================
```

### Event Types
- `COMMAND_RECEIVED`: Control command executed
- `VALIDATION_ERROR`: Invalid command rejected
- `SECURITY_VIOLATION`: Unauthorized access attempt
- `ERROR`: System error

## 🔷 Development & Testing

### Running Tests

**Test 1: Normal Operation**
```bash
# Start simulator
python3 grid_simulator.py

# In another terminal
curl -X POST http://localhost:5001/grid/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```

**Test 2: Security Block**
```bash
curl -X POST http://localhost:5001/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON"}'
```

**Test 3: Telemetry Polling**
```bash
watch -n 1 'curl -s http://localhost:5001/grid/data | jq'
```

### Configuration

**Port:** `5001` (default)
- Change in `grid_simulator.py`: `app.run(port=5001)`

**Telemetry Refresh Rate:** `1 second`
- Change in `grid_simulator.py`: `time.sleep(1)`

**Power Flow Factor:** `100.0`
- Change in `grid_simulator.py`: `CURRENT_FACTOR = 100.0`

## 🔷 Future Enhancements

This simulator is designed to integrate with:

1. **Cybersecurity Gateway** (Laptop-2)
   - Authentication & authorization
   - Command validation
   - Intrusion detection

2. **AI Engine**
   - Anomaly detection
   - Predictive threat analysis
   - Automated response

3. **Attack Simulation**
   - Man-in-the-middle attacks
   - Command injection
   - Replay attacks

## 🔷 License

This is a demonstration project for cybersecurity and AI research.

## 🔷 Contact

For questions or issues, please refer to the project documentation.

---

**⚡ Virtual Power Grid Simulator** - Demonstrating Cyber-Physical Security Architecture
