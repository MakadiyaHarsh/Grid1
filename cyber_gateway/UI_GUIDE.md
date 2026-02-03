# 🎨 Interactive Terminal UI - Quick Guide

## 🚀 Launch the UI

```bash
cd "/home/harsh/Documents/GRID-SHIELD AI/DEMO WIBE/cyber_gateway"
./venv/bin/python interactive_ui.py
```

## 📋 Features

### Main Menu Options

1. **Send Custom Command** - Enter your own breaker, voltage, and frequency values
2. **Send Preset Commands** - Choose from pre-configured test scenarios
3. **View Valid Ranges** - Display acceptable parameter ranges
4. **Check Gateway Health** - Verify system status
5. **Exit** - Close the application

### Custom Command Entry

- Interactive prompts with default values
- Real-time input validation
- Clear error messages
- Confirmation before sending

### Preset Commands

Choose from 7 pre-configured scenarios:
- ✅ Normal Operation
- ✅ Low Voltage
- ✅ High Voltage
- ✅ Breaker OFF
- 🚫 FDIA Attack (Will Block)
- 🚫 Voltage Violation (Will Block)
- 🚫 Frequency Violation (Will Block)

### Response Display

**Allowed Commands:**
- ✓ Green success message
- Risk score and attack type
- Updated grid state (breaker, voltage, frequency, power flow)

**Blocked Commands:**
- ✗ Red alert message
- Attack type and risk score
- Detailed reason for blocking

**Grid Errors:**
- ⚠ Yellow warning
- Security status (passed/failed)
- Connection troubleshooting info

## 🎯 Usage Examples

### Example 1: Send Custom Command

```
1. Select option 1 (Send Custom Command)
2. Enter breaker state: ON
3. Enter voltage: 1.02
4. Enter frequency: 50.1
5. Confirm and send
6. View formatted response
```

### Example 2: Test FDIA Attack

```
1. Select option 2 (Send Preset Commands)
2. Select option 5 (FDIA Attack)
3. View blocked response with security details
```

### Example 3: Check System Health

```
1. Select option 4 (Check Gateway Health)
2. View gateway and grid connection status
```

## 🎨 UI Features

- **Color-Coded Interface:**
  - 🔵 Blue: Information boxes
  - 🟢 Green: Success/allowed commands
  - 🔴 Red: Blocked/security alerts
  - 🟡 Yellow: Warnings/prompts
  - 🔷 Cyan: Headers and highlights

- **Input Validation:**
  - Automatic range checking
  - Type validation
  - Default value suggestions
  - Clear error messages

- **Formatted Output:**
  - Boxed displays
  - Aligned text
  - Color-coded status
  - Detailed response breakdown

## ⌨️ Keyboard Shortcuts

- `Ctrl+C` - Cancel current operation or exit
- `Enter` - Accept default value
- Number keys - Select menu options

## 🔧 Requirements

- Gateway must be running on port 5002
- Grid simulator should be running on port 5001 (optional)
- Python 3.10+ with requests library

## 📊 Valid Parameter Ranges

- **Voltage:** 0.90 - 1.10 pu
- **Frequency:** 49.0 - 51.0 Hz
- **Breaker:** ON or OFF
- **Risk Threshold:** 0.70

## 🎓 Tips

1. **Use Presets First** - Familiarize yourself with the system using preset commands
2. **Watch Terminal 2** - Keep gateway logs visible to see security events
3. **Test Attacks** - Try preset attack scenarios to see blocking in action
4. **Custom Values** - Experiment with custom values within valid ranges

## 🐛 Troubleshooting

**UI won't start:**
```bash
# Make sure you're using the virtual environment
./venv/bin/python interactive_ui.py
```

**Cannot connect to gateway:**
- Ensure gateway is running: `./venv/bin/python gateway.py`
- Check port 5002 is not blocked

**Grid connection errors:**
- This is normal if grid simulator is not running
- Commands will still be validated by security layers
- Start grid simulator for full functionality

---

**⚡ Enjoy the Interactive Experience!**
