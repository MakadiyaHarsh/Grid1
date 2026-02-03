# GRID-SHIELD AI — Integrated Cyber-Physical Security Platform

> **Industrial-grade cybersecurity platform combining Virtual Power Grid simulation, Multi-Model AI threat detection, and Cybersecurity Gateway enforcement.**

## 🎯 System Overview

GRID-SHIELD AI is a unified platform demonstrating advanced cyber-physical security for power grid systems. It integrates three independent subsystems into a cohesive architecture that detects and blocks sophisticated attacks (including FDIA) that traditional methods miss.

### Architecture

```
┌──────────────────────┐
│  ADMIN CONSOLE (CLI) │  ← Operator Interface
└─────────┬────────────┘
          │
          ▼
┌────────────────────────────┐
│ CYBERSECURITY GATEWAY      │
│  ├── Cyber Rules           │
│  ├── Attack Detection      │
│  ├── MULTI-AI ENGINE       │  ← 5 AI Models + Fusion
│  └── Decision Engine       │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│  VIRTUAL POWER GRID        │
│  Physical Execution Layer  │
└────────────────────────────┘
```

### Key Principles

✅ **Strict Layering**: AI never talks directly to grid; Grid never knows AI exists  
✅ **Gateway Enforcement**: All commands flow through cybersecurity gateway  
✅ **Explainable AI**: Every decision includes human-readable explanation  
✅ **Comprehensive Logging**: Cyber, AI, and Grid events logged separately  
✅ **Local Execution**: No cloud dependencies, deterministic operation  

## 📁 Directory Structure

```
GRID-SHIELD AI/DEMO-WIBE/
│
├── admin_console.py        ← Main executable entry point
├── start_system.sh         ← Helper script to launch all components
├── requirements.txt        ← Unified dependencies
│
├── cyber_gateway/
│   ├── gateway.py          ← Main gateway server (Port 5002)
│   ├── ai_interface.py     ← AI engine integration
│   ├── rules_engine.py     ← Cyber rules validation
│   ├── attack_detector.py  ← Traditional attack detection
│   ├── forwarder.py        ← Grid communication
│   ├── logger.py           ← Security event logging
│   └── config.py           ← Configuration
│
├── ai_engine/
│   ├── ai_pipeline.py      ← Main AI orchestrator
│   ├── fusion_engine.py    ← Multi-model fusion
│   ├── preprocessing.py    ← Data preprocessing
│   ├── config.py           ← AI configuration
│   └── models/
│       ├── anomaly_model.py
│       ├── fdia_model.py
│       ├── physics_model.py
│       ├── behavior_model.py
│       └── memory_model.py
│
├── virtual_grid/
│   ├── grid_simulator.py   ← Grid simulator (Port 5001)
│   └── templates/
│
└── logs/
    ├── cyber.log           ← Gateway security events
    ├── ai.log              ← AI analysis results
    └── grid.log            ← Grid execution events
```

## 🚀 Quick Start

### 1. Installation

```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO-WIBE"

# No manual installation needed!
# The launcher script handles everything automatically
```

### 2. Launch System

**Option A: Automated Launch (Recommended)**
```bash
./start_system.sh
```

**What this does:**
- ✅ Automatically creates/activates virtual environments
- ✅ Installs all dependencies (first run only)
- ✅ Starts all three servers
- ✅ Verifies server health
- ✅ Opens 3 terminal windows

**First-time setup:** ~1-2 minutes (creates venvs, installs packages)  
**Subsequent runs:** ~5 seconds (instant startup)

**Option B: Manual Launch**

Terminal 1 - Grid Simulator:
```bash
cd virtual_grid
source venv/bin/activate  # or .venv/bin/activate
python3 grid_simulator.py
```

Terminal 2 - Cybersecurity Gateway:
```bash
cd cyber_gateway
source venv/bin/activate
python3 gateway.py
```

Terminal 3 - Admin Console:
```bash
python3 admin_console.py
```

### 3. Stop System

```bash
./stop_system.sh
```

Cleanly stops all servers and cleans up processes.

### 3. Use Admin Console

The admin console provides 5 options:

1. **Send Operator Command** - Submit commands to the gateway
2. **View Live Grid Status** - Real-time telemetry monitoring
3. **View Cybersecurity Logs** - Gateway security events
4. **View AI Analysis Logs** - AI model outputs and decisions
5. **Exit** - Clean shutdown

## 🔬 Demonstration Scenarios

### Scenario 1: Normal Operation

**Objective**: Verify normal command flow

**Steps**:
1. In Admin Console, select Option 1 (Operator Command)
2. Enter: `Breaker=ON, Voltage=1.00, Frequency=50.0`

**Expected Result**:
- ✅ Cyber rules: PASS
- ✅ Attack detection: NONE
- ✅ AI risk: < 0.3 (SAFE)
- ✅ Decision: ALLOWED
- ✅ Grid state updated
- ✅ All logs show successful execution

### Scenario 2: FDIA Attack Detection

**Objective**: Demonstrate AI detection of False Data Injection Attack

**Background**: Traditional residual-based detection fails when attackers inject coordinated false data that maintains power flow equations. AI correlation analysis detects the attack.

**Steps**:
1. In Admin Console, select Option 1
2. Enter: `Breaker=ON, Voltage=1.08, Frequency=49.2`

**Expected Result**:
- ✅ Cyber rules: PASS (values within range)
- ✅ Traditional residual: PASS (no anomaly)
- ❌ AI FDIA model: TRIGGER (voltage-frequency correlation violated)
- ❌ Fusion risk: > 0.7
- ❌ Decision: **BLOCKED**
- ✅ Logs show "AI CRITICAL: FDIA detected"

**Why This Matters**: This demonstrates the core value proposition - AI detects attacks that bypass traditional security.

### Scenario 3: Live Monitoring

**Objective**: Monitor real-time grid telemetry

**Steps**:
1. In Admin Console, select Option 2 (Live Grid Monitor)
2. In another terminal, send commands via curl or Admin Console
3. Observe real-time updates

**Expected Result**:
- Display refreshes every 1 second
- Voltage, frequency, breaker, power flow shown
- Color-coded status indicators
- Press Ctrl+C to exit

### Scenario 4: Log Analysis

**Objective**: Review historical security events

**Steps**:
1. After running Scenarios 1-2, select Option 3 (Cybersecurity Logs)
2. Review blocked and allowed events
3. Select Option 4 (AI Logs)
4. Review AI model outputs and fusion results

**Expected Result**:
- Cyber logs show all gateway decisions
- AI logs show model scores and explanations
- Blocked attacks highlighted in red
- Timestamps consistent across all logs

## 🔌 API Endpoints

### Cybersecurity Gateway (Port 5002)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/operator/command` | POST | Submit operator command (goes through full security pipeline) |
| `/health` | GET | Gateway health check |

### Virtual Grid (Port 5001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/grid/command` | POST | Grid control (gateway access only) |
| `/grid/data` | GET | Read-only telemetry |
| `/operator/command` | POST | **BLOCKED** (security violation) |

## 🧠 AI Engine Details

### Five Specialized Models

1. **Anomaly Detection** - Statistical deviation analysis
2. **FDIA Detection** - Correlation-based attack detection
3. **Physics Validation** - Power system law enforcement
4. **Behavior Learning** - Operator pattern analysis
5. **Memory & Similarity** - Historical attack matching

### Fusion Engine

Combines all model outputs using weighted fusion:
- FDIA: 35% (highest priority)
- Physics: 25%
- Anomaly: 15%
- Memory: 15%
- Behavior: 10%

### Decision Thresholds

- **SAFE**: Risk < 0.30
- **WARNING**: 0.30 ≤ Risk < 0.60
- **CRITICAL**: Risk ≥ 0.60 (command blocked)

## 📊 Logging System

### Cyber Log (`logs/cyber.log`)
```
[2026-01-31 03:20:15] BLOCKED — FDIA_SUSPECTED (Risk: 0.82)
[2026-01-31 03:20:15] REASON: AI CRITICAL: FDIA detected - voltage-frequency correlation violated
```

### AI Log (`logs/ai.log`)
```
[2026-01-31 03:20:15] AI RISK 0.82 — CRITICAL
[2026-01-31 03:20:15] EXPLANATION: FDIA detected - voltage-frequency correlation violated
[2026-01-31 03:20:15] MODEL OUTPUTS: Anomaly=0.15, FDIA=0.89, Physics=0.22, Behavior=0.05, Memory=0.12
```

### Grid Log (`logs/grid.log`)
```
[2026-01-31 03:20:10] COMMAND_RECEIVED — {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}
[2026-01-31 03:20:10] Safe execution
```

## 🛡️ Security Model

### Defense Layers

1. **Cyber Rules** - Range validation, format checking
2. **Attack Detection** - Replay attack, injection detection
3. **AI Analysis** - Multi-model threat assessment
4. **Decision Engine** - Combined risk evaluation
5. **Grid Isolation** - Physical layer protection

### Why Traditional Detection Fails

Traditional methods rely on **residual-based detection**:
```
residual = measured_value - expected_value
if residual > threshold: ATTACK
```

**FDIA bypasses this** by injecting coordinated false data that satisfies power flow equations, making residual ≈ 0.

**AI detects FDIA** by analyzing:
- Voltage-frequency correlation
- Temporal consistency
- Multi-signal coordination
- Historical patterns

## 🔧 Configuration

### Gateway Config (`cyber_gateway/config.py`)

```python
RISK_THRESHOLD = 0.70        # Block if risk > 0.70
AI_RISK_WEIGHT = 1.2         # AI scores weighted higher
VOLTAGE_MIN = 0.90           # Per-unit
VOLTAGE_MAX = 1.10
FREQUENCY_MIN = 49.0         # Hz
FREQUENCY_MAX = 51.0
```

### AI Config (`ai_engine/config.py`)

```python
FUSION_WEIGHTS = {
    'fdia': 0.35,      # Highest priority
    'physics': 0.25,
    'anomaly': 0.15,
    'memory': 0.15,
    'behavior': 0.10
}
```

## 🎓 Educational Value

This platform demonstrates:

1. **Cyber-Physical Security** - Integration of IT and OT security
2. **AI in Critical Infrastructure** - Explainable AI for safety-critical systems
3. **Defense in Depth** - Multiple security layers
4. **FDIA Detection** - Advanced attack detection beyond traditional methods
5. **Industrial Architecture** - Real-world system design patterns

## 📝 Development Notes

- **No Cloud Dependencies** - Fully local execution
- **Deterministic** - Reproducible results for research
- **Modular** - Each component can be developed independently
- **Explainable** - All decisions include human-readable explanations
- **Logged** - Complete audit trail for analysis

## 🤝 Contributing

This is a research/demonstration platform. Key areas for enhancement:

- Additional AI models (e.g., deep learning)
- More sophisticated grid simulation
- Advanced attack scenarios
- Performance optimization
- UI/dashboard development

## 📄 License

Research and educational use.

---

**Built with ❤️ for advancing cyber-physical security research**
