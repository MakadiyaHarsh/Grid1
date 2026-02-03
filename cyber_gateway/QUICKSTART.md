# Quick Start Guide - Cybersecurity Gateway

## Prerequisites

- Python 3.10+
- Virtual Power Grid Simulator (optional, for full integration)

## Installation

```bash
cd cyber_gateway

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Gateway

```bash
# Make sure you're in the cyber_gateway directory
cd cyber_gateway

# Activate virtual environment
source venv/bin/activate

# Start the gateway
python gateway.py
```

**Expected Output:**
```
================================================================================
CYBERSECURITY GATEWAY FOR POWER GRID SYSTEM
================================================================================
Gateway Server: http://0.0.0.0:5002
Grid Simulator: http://localhost:6001
Risk Threshold: 0.7
================================================================================

[INFO] 2026-01-31 02:08:22 - Cybersecurity Gateway starting...
[INFO] 2026-01-31 02:08:22 - Operator endpoint: POST /operator/command
[INFO] 2026-01-31 02:08:22 - Gateway is OPERATIONAL and ready to receive commands
```

## Testing

### Option 1: Run Automated Demo

```bash
./demo.sh
```

This will run all test scenarios automatically.

### Option 2: Manual Testing

**Test Normal Command:**
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.02, "frequency": 50.1}'
```

**Test Voltage Violation:**
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.25, "frequency": 50.0}'
```

**Test FDIA Attack:**
```bash
curl -X POST http://localhost:5002/operator/command \
  -H "Content-Type: application/json" \
  -d '{"breaker": "ON", "voltage": 1.10, "frequency": 51.0}'
```

**Test Replay Attack:**
```bash
for i in {1..5}; do
  curl -X POST http://localhost:5002/operator/command \
    -H "Content-Type: application/json" \
    -d '{"breaker": "ON", "voltage": 1.0, "frequency": 50.0}'
  sleep 0.5
done
```

## Integration with Grid Simulator

If you have the Virtual Power Grid Simulator running:

1. **Start Grid Simulator** (in another terminal):
   ```bash
   cd ../virtual_grid
   python grid_simulator.py
   ```
   Grid should be running on port 5001.

2. **Start Gateway** (in this terminal):
   ```bash
   python gateway.py
   ```

3. **Send Commands:**
   Commands will now be forwarded to the grid simulator.

## Configuration

Edit `config.py` to customize:

- **Grid connection:** `GRID_HOST`, `GRID_PORT`
- **Security thresholds:** `RISK_THRESHOLD`
- **Cyber rules:** `VOLTAGE_MIN`, `VOLTAGE_MAX`, `FREQUENCY_MIN`, `FREQUENCY_MAX`
- **Attack detection:** `REPLAY_WINDOW_SECONDS`, `REPLAY_COUNT_THRESHOLD`

## Stopping the Gateway

Press `Ctrl+C` in the terminal running the gateway.

## Troubleshooting

**Port already in use:**
- Change `GATEWAY_PORT` in `config.py`

**Cannot connect to grid:**
- Ensure grid simulator is running on port 6001
- Check `GRID_PORT` in `config.py`

**Import errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

## API Endpoints

- **POST /operator/command** - Submit operator commands
- **GET /health** - Check gateway and grid health
- **GET /** - Gateway status and info

## Security Features

✅ Cyber rules validation  
✅ Attack detection (FDIA, Replay, Data Manipulation)  
✅ Risk-based decision making  
✅ Comprehensive security logging  
✅ Grid forwarding with error handling  

---

For detailed documentation, see [README.md](README.md)
