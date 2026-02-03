# GRID-SHIELD AI — Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO-WIBE"
pip install -r requirements.txt
```

### Step 2: Launch System

```bash
./start_system.sh
```

**What this does automatically:**
- ✅ Checks/creates virtual environments for each component
- ✅ Installs all required dependencies
- ✅ Starts Virtual Grid Simulator (Port 5001)
- ✅ Starts Cybersecurity Gateway (Port 5002)
- ✅ Starts Admin Console (Interactive)
- ✅ Verifies all servers are running
- ✅ Opens 3 terminal windows automatically

**First-time setup:** The script will automatically create virtual environments and install dependencies. This may take 1-2 minutes on first run.

**Subsequent runs:** Instant startup - environments are already configured!

### Step 3: Send Your First Command

In the **Admin Console** window:

1. Select option `1` (Send operator command)
2. Enter:
   - Breaker: `ON`
   - Voltage: `1.00`
   - Frequency: `50.0`
3. Observe the AI analysis and decision

✅ **Expected**: Command ALLOWED, grid state updated

### Step 4: Try an FDIA Attack

1. Select option `1` again
2. Enter:
   - Breaker: `ON`
   - Voltage: `1.08`
   - Frequency: `49.2`
3. Observe AI detection

❌ **Expected**: Command BLOCKED by AI (FDIA detected)

### Step 5: Monitor Live Grid

1. Select option `2` (View live grid status)
2. Watch real-time telemetry updates
3. Press `Ctrl+C` to exit monitor

### Step 6: Review Logs

1. Select option `3` (Cybersecurity logs) - See blocked attacks
2. Select option `4` (AI logs) - See AI model outputs

## 📖 What Just Happened?

### Normal Command Flow
```
Operator → Gateway → Cyber Rules ✅ → Attack Detection ✅ → AI Analysis ✅ → Grid ✅
```

### FDIA Attack Blocked
```
Operator → Gateway → Cyber Rules ✅ → Attack Detection ✅ → AI Analysis ❌ → BLOCKED
                                                              ↑
                                                    AI detected correlation violation
```

## 🎯 Key Demonstrations

### Demo 1: Why Traditional Security Fails

**Traditional Method**: Check if values are in range
- Voltage 1.08 pu → ✅ PASS (0.90-1.10 range)
- Frequency 49.2 Hz → ✅ PASS (49.0-51.0 range)
- **Result**: ALLOWED ❌ (Attack succeeds)

**GRID-SHIELD AI**: Check correlations and physics
- Voltage-Frequency correlation → ❌ FAIL (uncorrelated)
- AI FDIA Model → ❌ TRIGGER (Risk: 0.89)
- **Result**: BLOCKED ✅ (Attack prevented)

### Demo 2: Explainable AI

Every AI decision includes:
- **Risk Score**: 0.0 to 1.0
- **Decision**: SAFE / WARNING / CRITICAL
- **Explanation**: Human-readable reason
- **Model Outputs**: Individual model scores
- **Confidence**: Decision confidence level

Example:
```json
{
  "decision": "CRITICAL",
  "risk_score": 0.82,
  "explanation": "FDIA detected - voltage-frequency correlation violated",
  "model_outputs": {
    "anomaly": 0.15,
    "fdia": 0.89,
    "physics": 0.22,
    "behavior": 0.05,
    "memory": 0.12
  },
  "confidence": 0.94
}
```

## 🔍 Troubleshooting

### "Cannot connect to gateway"
- Ensure gateway is running: Check the Gateway terminal window
- Check port 5002 is not in use: `lsof -i :5002`
- Restart system: `./stop_system.sh` then `./start_system.sh`

### "Cannot connect to grid"
- Ensure grid is running: Check the Grid terminal window
- Check port 5001 is not in use: `lsof -i :5001`
- Restart system: `./stop_system.sh` then `./start_system.sh`

### "AI engine unavailable"
- The launcher installs dependencies automatically
- If issues persist, manually run: `pip install -r requirements.txt`

### Stop All Servers
```bash
./stop_system.sh
```
This will cleanly stop all running servers and clean up processes.

## 📚 Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Try Attack Scenarios**: Test different attack patterns
3. **Review Logs**: Analyze `logs/` directory
4. **Customize AI**: Modify `ai_engine/config.py`
5. **Add Models**: Extend `ai_engine/models/`

## 🎓 Learning Path

1. ✅ **Basic Operation** - Send normal commands
2. ✅ **Attack Detection** - Try FDIA attacks
3. 📊 **Log Analysis** - Review security events
4. 🧠 **AI Understanding** - Study model outputs
5. ⚙️ **Configuration** - Tune thresholds and weights
6. 🔬 **Research** - Develop new attack scenarios

---

**Ready to explore? Start with `./start_system.sh`!**
