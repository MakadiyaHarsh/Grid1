# GRID-SHIELD AI - Investor Demo Guide

## 🎯 Demo Overview

This guide provides a step-by-step demonstration script for showcasing GRID-SHIELD AI's comprehensive cybersecurity capabilities to investors.

## 🚀 Quick Start

### 1. Launch the System

```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO-WIBE"
./start_system.sh
```

This will open **4 terminal windows**:
1. **Grid Simulator** (Port 5001) - Virtual power grid
2. **Cybersecurity Gateway** (Port 5002) - Security layer with AI
3. **Admin Console** - Operator interface
4. **Attack Simulator** - Cyber attack demonstration tool

### 2. Verify System Status

Check that all terminals show "running" or "operational" status.

---

## 📋 Demo Script (15 minutes)

### Part 1: System Architecture (2 minutes)

**Show the 4 terminals and explain:**

> "GRID-SHIELD AI is a three-layer cyber-physical security platform:
> 
> 1. **Virtual Power Grid** - Simulates real substation operations
> 2. **Cybersecurity Gateway** - Multi-layered defense with AI integration
> 3. **Admin Console** - Secure operator interface
> 4. **Attack Simulator** - For security testing and demonstrations"

### Part 2: Normal Operation (3 minutes)

**In Admin Console (Terminal 3):**

1. Select option `1` (Send operator command)
2. Enter normal parameters:
   - Breaker: `ON`
   - Voltage: `1.00`
   - Frequency: `50.0`

**Point out:**
- ✅ Status: ALLOWED
- Low risk score
- Command forwarded to grid
- Grid state updated successfully

> "Under normal conditions, legitimate operator commands pass through seamlessly."

### Part 3: Attack Demonstrations (8 minutes)

**Switch to Attack Simulator (Terminal 4)**

#### Attack 1: FDIA (False Data Injection)

1. Select option `1` (FDIA Attack)
2. Press Enter to launch

**Explain:**
> "FDIA attacks are sophisticated - they inject false data that maintains power flow equations, bypassing traditional detection. Our **AI engine** detects these through correlation analysis."

**Show the result:**
- 🛡️ ATTACK BLOCKED
- AI detected correlation violation
- High risk score

#### Attack 2: Replay Attack

1. Select option `2` (Replay Attack)
2. Press Enter to launch

**Explain:**
> "Replay attacks rapidly repeat legitimate commands. Our **attack detector** identifies this pattern through command history analysis."

**Show the result:**
- First few attempts may pass
- Subsequent attempts BLOCKED
- "Replay attack detected" message

#### Attack 3: Multi-Vector Attack

1. Select option `8` (Multi-Vector Attack)
2. Press Enter to launch

**Explain:**
> "Real attackers use multiple techniques simultaneously. Watch how our system handles 5 different attack vectors in sequence."

**Show the results:**
- Multiple attacks blocked
- Different detection methods triggered
- Comprehensive defense demonstrated

### Part 4: Automated Investor Demo (2 minutes)

**In Attack Simulator:**

1. Select option `9` (Investor Demo)
2. Press Enter to start automated demo

**Sit back and let it run:**
- Shows 6 pre-configured scenarios
- Demonstrates normal operation vs attacks
- Automated visual presentation

**Explain:**
> "This automated demo shows the complete threat landscape - from normal operations to sophisticated multi-stage attacks."

---

## 🎨 Visual Highlights

### Color Coding

- **🟢 GREEN** = Allowed/Safe
- **🔴 RED** = Blocked/Attack
- **🟡 YELLOW** = Warning/Elevated Risk
- **🔵 CYAN** = Information

### Key Metrics to Point Out

1. **Risk Score** (0.0 - 1.0)
   - < 0.3 = Safe
   - 0.3 - 0.6 = Warning
   - \> 0.6 = Critical

2. **Attack Types Detected**
   - FDIA (AI-based detection)
   - Replay Attack
   - Data Manipulation
   - Parameter Injection
   - Correlation Anomaly

3. **AI Analysis**
   - Decision: SAFE/WARNING/CRITICAL
   - Confidence score
   - Explanation of reasoning

---

## 💡 Key Talking Points

### 1. Multi-Layered Defense

> "Unlike traditional systems that rely on a single detection method, GRID-SHIELD AI uses **5 layers of defense**:
> 
> 1. Cyber Rules Validation
> 2. Attack Pattern Detection
> 3. AI Multi-Model Analysis
> 4. Physics-Aware Validation
> 5. Behavioral Learning"

### 2. AI Advantage

> "Our **Multi-Model AI Engine** uses 5 specialized models:
> 
> - Anomaly Detection (statistical)
> - FDIA Detection (correlation-based)
> - Physics Validation (domain knowledge)
> - Behavioral Learning (pattern recognition)
> - Memory System (historical comparison)
> 
> This catches sophisticated attacks that bypass traditional methods."

### 3. Explainability

> "Every decision includes a **human-readable explanation**. Operators understand *why* a command was blocked, enabling faster incident response."

### 4. Real-Time Performance

> "All analysis happens in **real-time** - typically under 100ms. No cloud dependency, all processing is local for security and reliability."

---

## 🔧 Advanced Demo Options

### Live Grid Monitoring

**In Admin Console:**
1. Select option `2` (Live Grid Monitor)
2. Show real-time telemetry updates
3. Press Ctrl+C to exit

### Log Viewing

**In Admin Console:**
1. Select option `3` (Cybersecurity Logs)
2. Show blocked attack events highlighted in red
3. Select option `4` (AI Logs)
4. Show AI analysis decisions

---

## 🌐 Remote Attack Demo (Optional)

For advanced demonstrations from another machine:

### Setup

1. **Find your IP address:**
   ```bash
   ip addr show | grep "inet "
   ```

2. **Update gateway config** to listen on all interfaces:
   ```python
   # In cyber_gateway/config.py
   GATEWAY_HOST = "0.0.0.0"  # Already configured
   ```

3. **From remote machine**, use the attack simulator:
   ```bash
   # Modify GATEWAY_URL in attack_simulator.py
   GATEWAY_URL = "http://YOUR_IP:5002"
   ```

### Firewall Configuration

```bash
# Allow ports 5001 and 5002
sudo ufw allow 5001/tcp
sudo ufw allow 5002/tcp
```

---

## 📊 Attack Type Reference

| Attack Type | Detection Method | Typical Risk Score |
|------------|------------------|-------------------|
| **FDIA** | AI Correlation Analysis | 0.75 - 0.90 |
| **Replay** | Command History | 0.60 - 0.90 |
| **Data Manipulation** | Spike Detection | 0.70 - 0.80 |
| **Parameter Injection** | Cyber Rules | 1.00 (immediate) |
| **Correlation** | Anomaly Detection | 0.65 - 0.75 |
| **DoS/Flooding** | Rate Limiting | 0.60 - 0.80 |
| **Spoofing** | Pattern Analysis | 0.65 - 0.85 |

---

## 🎬 Closing the Demo

1. **Stop the attack simulator** (Option 0)
2. **Show the logs** in Admin Console
3. **Stop the system:**
   ```bash
   ./stop_system.sh
   ```

### Final Message

> "GRID-SHIELD AI provides **industrial-grade protection** for critical infrastructure. Our multi-layered approach with AI integration catches both traditional and sophisticated attacks, while maintaining **explainability** and **real-time performance**."

---

## 🆘 Troubleshooting

### Terminals close immediately
- Check Python errors in terminal output
- Verify virtual environment is activated
- Run `./launch_grid.sh` manually to see errors

### Gateway not responding
- Check if port 5002 is in use: `lsof -i:5002`
- Verify gateway terminal shows "operational"
- Wait 5 seconds after launch

### Attack simulator connection errors
- Ensure gateway is running first
- Check GATEWAY_URL in attack_simulator.py
- Verify no firewall blocking localhost

---

## 📞 Support

For technical issues during demo:
- Check `logs/cyber.log` for gateway errors
- Check `logs/ai.log` for AI engine errors
- Check `logs/grid.log` for grid simulator errors
