# 📚 GRID-SHIELD AI - Documentation Index

## 🎯 Quick Access

### 🎨 Interactive Terminal UI (NEW!)
**The easiest way to use the system:**
```bash
./start_ui.sh
```
- Graphical terminal interface with colored menus
- Input validation and default values
- 7 preset test scenarios
- Real-time formatted responses
- See [UI_GUIDE.md](UI_GUIDE.md) for details

### For First-Time Users
1. **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
2. **[cheatsheet.sh](cheatsheet.sh)** - Run this for quick command reference
   ```bash
   ./cheatsheet.sh
   ```

### For Daily Operations
1. **[interactive_ui.py](interactive_ui.py)** - Interactive terminal UI (recommended)
2. **[COMMANDS.md](COMMANDS.md)** - Complete command reference
3. **[demo.sh](demo.sh)** - Automated testing script
   ```bash
   ./demo.sh
   ```

### For Understanding the System
1. **[README.md](README.md)** - Full system documentation
2. **[SYSTEM_STATUS.md](SYSTEM_STATUS.md)** - Current system status and capabilities

---

## 📖 Documentation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| **UI_GUIDE.md** | Interactive terminal UI guide | Using the graphical interface |
| **QUICKSTART.md** | Installation and basic setup | First time setup |
| **COMMANDS.md** | All operational commands | Daily operations, testing |
| **README.md** | Complete documentation | Understanding architecture |
| **SYSTEM_STATUS.md** | System capabilities and status | Demonstrations, reviews |
| **cheatsheet.sh** | Quick command reference | Quick lookup |
| **demo.sh** | Automated testing | Running all tests |
| **start_ui.sh** | Launch interactive UI | Easy command entry |

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Grid Simulator
```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO WIBE/virtual_grid"
./venv/bin/python grid_simulator.py
```

### Step 2: Start Gateway (New Terminal)
```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO WIBE/cyber_gateway"
./venv/bin/python gateway.py
```

### Step 3: Send Test Command (New Terminal)
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```

---

## 📋 Common Tasks

### View Quick Commands
```bash
./cheatsheet.sh
```

### Run All Tests
```bash
./demo.sh
```

### Check System Health
```bash
curl http://localhost:5002/health
```

### View Grid State
```bash
curl http://localhost:5001/grid/data
```

### Send Command
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0, "frequency": 50.0}'
```

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| **config.py** | Gateway configuration (ports, thresholds, ranges) |
| **requirements.txt** | Python dependencies |

---

## 💻 Source Code Files

| File | Purpose | Lines |
|------|---------|-------|
| **gateway.py** | Main Flask server | ~200 |
| **rules_engine.py** | Cyber rule validation | ~150 |
| **attack_detector.py** | Attack detection algorithms | ~250 |
| **forwarder.py** | Grid communication | ~80 |
| **logger.py** | Security event logging | ~100 |
| **config.py** | Configuration | ~35 |

---

## 🎓 For Academic/Research Use

### Demonstration
1. Start both systems (see Quick Start above)
2. Run `./demo.sh` to show all security features
3. Watch Terminal 2 for security event logs
4. Show blocked vs allowed commands

### Documentation for Papers/Presentations
- **Architecture:** See README.md "System Architecture" section
- **Security Features:** See SYSTEM_STATUS.md "Security Layers" section
- **Test Results:** See SYSTEM_STATUS.md "Successfully Demonstrated Features"
- **API Documentation:** See README.md "API Documentation" section

---

## 🔍 Troubleshooting

### System Won't Start
1. Check if ports are available: `lsof -i :5001` and `lsof -i :5002`
2. Ensure virtual environment is activated
3. Check if dependencies are installed: `pip list`

### Commands Not Working
1. Verify both systems are running
2. Check system health: `curl http://localhost:5002/health`
3. Review parameter ranges in COMMANDS.md

### Need Help?
- See **Troubleshooting** section in README.md
- See **Troubleshooting Commands** in COMMANDS.md

---

## 📊 System Information

- **Gateway Port:** 5002
- **Grid Simulator Port:** 5001
- **Risk Threshold:** 0.70
- **Voltage Range:** 0.90 - 1.10 pu
- **Frequency Range:** 49.0 - 51.0 Hz

---

## 🎯 File Organization

```
cyber_gateway/
│
├── 📚 Documentation
│   ├── INDEX.md              ← You are here
│   ├── QUICKSTART.md         ← Start here for setup
│   ├── COMMANDS.md           ← All commands
│   ├── README.md             ← Full documentation
│   └── SYSTEM_STATUS.md      ← System capabilities
│
├── 🔧 Scripts
│   ├── cheatsheet.sh         ← Quick reference
│   └── demo.sh               ← Automated tests
│
├── 💻 Source Code
│   ├── gateway.py            ← Main server
│   ├── config.py             ← Configuration
│   ├── rules_engine.py       ← Cyber rules
│   ├── attack_detector.py    ← Attack detection
│   ├── forwarder.py          ← Grid communication
│   └── logger.py             ← Security logging
│
└── ⚙️ Configuration
    ├── requirements.txt      ← Dependencies
    └── venv/                 ← Virtual environment
```

---

## ⚡ Quick Reference Card

### URLs
- Gateway: `http://localhost:5002/operator/command`
- Grid Data: `http://localhost:5001/grid/data`
- Health: `http://localhost:5002/health`

### Command Template
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.0, "frequency": 50.0}'
```

### Valid Ranges
- Voltage: 0.90 - 1.10 pu
- Frequency: 49.0 - 51.0 Hz
- Breaker: "ON" or "OFF"

---

**⚡ GRID-SHIELD AI - Protecting Critical Infrastructure**

*For questions or issues, refer to the appropriate documentation file above.*
