#!/usr/bin/env python3
"""
Virtual Power Grid Simulator
=============================
A realistic electrical grid control system simulator for cybersecurity and AI research.

This component represents the Physical Power Grid + Substation Execution Layer.
It simulates realistic grid behavior, processes control commands, and generates telemetry.

Architecture:
    Operator System → Cybersecurity Gateway (Laptop-2) → Virtual Power Grid (Laptop-3)

Security Model:
    - Direct operator access is BLOCKED
    - Only cybersecurity gateway can send control commands
    - Read-only telemetry available to all authorized systems
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import threading
import time
import json
import os

app = Flask(__name__)

# ============================================================================
# GRID STATE MODEL
# ============================================================================

grid_state = {
    "voltage": 0.0,          # Per-unit value (0.90 - 1.10 normal range)
    "frequency": 0.0,        # Hz (49.0 - 51.0 normal range)
    "breaker": "OFF",        # ON / OFF
    "power_flow": 0.0,       # MW (derived from voltage × current factor)
    "last_update": 0         # Unix timestamp
}

# Thread lock for safe concurrent access
state_lock = threading.Lock()

# Current factor for power flow calculation (simplified model)
CURRENT_FACTOR = 100.0  # Multiplier to convert voltage to MW

# Setup grid logging
GRID_LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'grid.log')
os.makedirs(os.path.dirname(GRID_LOG_PATH), exist_ok=True)

def write_grid_log(message):
    """Write to grid log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(GRID_LOG_PATH, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

# ============================================================================
# REALISTIC POWER SYSTEM BEHAVIOR
# ============================================================================

def update_grid_state(breaker=None, voltage=None, frequency=None):
    """
    Update grid state with realistic electrical behavior.
    
    Electrical Logic:
    - When breaker is OFF: voltage=0, frequency=0, power_flow=0
    - When breaker is ON: commanded values applied, power_flow calculated
    
    Args:
        breaker (str): "ON" or "OFF"
        voltage (float): Per-unit voltage (0.90 - 1.10)
        frequency (float): Frequency in Hz (49.0 - 51.0)
    
    Returns:
        dict: Updated grid state
    """
    with state_lock:
        # Update breaker state if provided
        if breaker is not None:
            grid_state["breaker"] = breaker.upper()
        
        # Apply realistic electrical behavior
        if grid_state["breaker"] == "OFF":
            # Breaker open: no voltage, frequency, or power flow
            grid_state["voltage"] = 0.0
            grid_state["frequency"] = 0.0
            grid_state["power_flow"] = 0.0
        else:
            # Breaker closed: apply commanded values
            if voltage is not None:
                grid_state["voltage"] = voltage
            if frequency is not None:
                grid_state["frequency"] = frequency
            
            # Calculate power flow (simplified: P = V × I_factor)
            grid_state["power_flow"] = grid_state["voltage"] * CURRENT_FACTOR
        
        # Update timestamp
        grid_state["last_update"] = time.time()
        
        return grid_state.copy()

def validate_command(data):
    """
    Validate control command parameters.
    
    Args:
        data (dict): Command data
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if "breaker" in data:
        if data["breaker"].upper() not in ["ON", "OFF"]:
            return False, "Invalid breaker state. Must be 'ON' or 'OFF'"
    
    if "voltage" in data:
        voltage = data["voltage"]
        if not isinstance(voltage, (int, float)):
            return False, "Voltage must be a number"
        if voltage < 0.90 or voltage > 1.10:
            return False, f"Voltage out of range. Must be 0.90-1.10 pu (received: {voltage})"
    
    if "frequency" in data:
        frequency = data["frequency"]
        if not isinstance(frequency, (int, float)):
            return False, "Frequency must be a number"
        if frequency < 49.0 or frequency > 51.0:
            return False, f"Frequency out of range. Must be 49.0-51.0 Hz (received: {frequency})"
    
    return True, None

# ============================================================================
# TELEMETRY GENERATION (AUTO-REFRESH)
# ============================================================================

def telemetry_updater():
    """
    Background thread that updates telemetry timestamp every second.
    This enables continuous real-time monitoring.
    """
    while True:
        time.sleep(1)
        with state_lock:
            grid_state["last_update"] = time.time()

# Start telemetry updater thread
telemetry_thread = threading.Thread(target=telemetry_updater, daemon=True)
telemetry_thread.start()

# ============================================================================
# EVENT LOGGING
# ============================================================================

def log_event(event_type, details):
    """
    Log grid events to terminal with formatted output.
    
    Args:
        event_type (str): Type of event (COMMAND, STATE_CHANGE, SECURITY, etc.)
        details (dict): Event details
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write to file
    write_grid_log(f"{event_type} — {json.dumps(details)}")
    
    # Print to terminal
    print("\n" + "="*60)
    print(f"⚡ GRID EVENT - {event_type}")
    print(f"Timestamp: {timestamp}")
    print("-"*60)
    for key, value in details.items():
        print(f"{key}: {value}")
    print("="*60)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def dashboard():
    """Serve the optional dashboard interface."""
    return render_template('dashboard.html')

@app.route('/grid/command', methods=['POST'])
def grid_command():
    """
    Control command endpoint (GATEWAY ACCESS ONLY).
    
    This endpoint accepts control commands from the cybersecurity gateway.
    It updates the grid state and returns the new state.
    
    Request Body:
        {
            "breaker": "ON" | "OFF",
            "voltage": float (0.90-1.10),
            "frequency": float (49.0-51.0)
        }
    
    Returns:
        JSON response with updated grid state
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "ERROR",
                "message": "No data provided"
            }), 400
        
        # Validate command
        is_valid, error_msg = validate_command(data)
        if not is_valid:
            log_event("VALIDATION_ERROR", {
                "Error": error_msg,
                "Received Data": json.dumps(data)
            })
            return jsonify({
                "status": "ERROR",
                "message": error_msg
            }), 400
        
        # Update grid state
        new_state = update_grid_state(
            breaker=data.get("breaker"),
            voltage=data.get("voltage"),
            frequency=data.get("frequency")
        )
        
        # Log the command execution
        log_event("COMMAND_RECEIVED", {
            "Source": "Cybersecurity Gateway",
            "Breaker": new_state["breaker"],
            "Voltage": f"{new_state['voltage']:.2f} pu",
            "Frequency": f"{new_state['frequency']:.1f} Hz",
            "Power Flow": f"{new_state['power_flow']:.2f} MW"
        })
        
        return jsonify({
            "status": "SUCCESS",
            "message": "Grid state updated",
            "grid_state": new_state
        }), 200
        
    except Exception as e:
        log_event("ERROR", {
            "Exception": str(e),
            "Type": type(e).__name__
        })
        return jsonify({
            "status": "ERROR",
            "message": f"Internal error: {str(e)}"
        }), 500

@app.route('/grid/data', methods=['GET'])
def grid_data():
    """
    Read-only telemetry endpoint.
    
    This endpoint provides real-time grid telemetry data.
    It can be accessed by dashboards, AI engines, and monitoring systems.
    
    Returns:
        JSON response with current grid state
    """
    with state_lock:
        current_state = grid_state.copy()
    
    return jsonify({
        "status": "SUCCESS",
        "grid_state": current_state,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/operator/command', methods=['POST'])
def operator_command():
    """
    SECURITY BLOCK: Direct operator access endpoint.
    
    This endpoint ALWAYS denies access to demonstrate that direct operator
    access is not allowed. All commands must flow through the cybersecurity gateway.
    
    Returns:
        JSON response with denial message
    """
    try:
        data = request.get_json()
        
        # Log security violation attempt
        log_event("SECURITY_VIOLATION", {
            "Attempt": "Direct operator access",
            "Endpoint": "/operator/command",
            "Status": "DENIED",
            "Reason": "Direct operator access not allowed",
            "Attempted Data": json.dumps(data) if data else "None"
        })
        
    except:
        pass  # Even if parsing fails, still deny
    
    return jsonify({
        "status": "DENIED",
        "reason": "Direct operator access not allowed"
    }), 403

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("⚡ VIRTUAL POWER GRID SIMULATOR")
    print("="*60)
    print("Status: INITIALIZING")
    print("Grid State: OFFLINE")
    print("Breaker: OFF")
    print("Voltage: 0.00 pu")
    print("Frequency: 0.00 Hz")
    print("Power Flow: 0.00 MW")
    print("="*60)
    print("\nEndpoints:")
    print("  POST /grid/command     → Gateway control access")
    print("  GET  /grid/data        → Read-only telemetry")
    print("  POST /operator/command → BLOCKED (security)")
    print("  GET  /                 → Dashboard (optional)")
    print("\nListening on: http://localhost:5001")
    print("="*60 + "\n")
    
    # Start Flask application
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
