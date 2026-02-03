#!/usr/bin/env python3
"""
GRID-SHIELD AI Admin Console
=============================
Terminal-based administrative interface for the integrated cyber-physical platform.

Features:
1. Operator Command Panel - Send commands to cybersecurity gateway
2. Live Grid Monitor - Real-time telemetry monitoring
3. Cybersecurity Logs Viewer - View gateway security events
4. AI Logs Viewer - View AI analysis results
5. Exit - Clean shutdown
"""

import requests
import time
import os
import sys
import json
from datetime import datetime

# Configuration
GATEWAY_URL = "http://localhost:5002"
GRID_URL = "http://localhost:5001"
CYBER_LOG_PATH = "logs/cyber.log"
AI_LOG_PATH = "logs/ai.log"
GRID_LOG_PATH = "logs/grid.log"

# ANSI Color Codes
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Print application header"""
    clear_screen()
    print(Colors.CYAN + "=" * 80 + Colors.RESET)
    print(Colors.BOLD + Colors.GREEN + " GRID-SHIELD AI CYBER SECURITY PLATFORM" + Colors.RESET)
    print(Colors.CYAN + "=" * 80 + Colors.RESET)
    print()

def print_menu():
    """Print main menu"""
    print_header()
    print(f"{Colors.YELLOW}Main Menu:{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}1️⃣{Colors.RESET}  Send operator command")
    print(f"  {Colors.BOLD}2️⃣{Colors.RESET}  View live grid status")
    print(f"  {Colors.BOLD}3️⃣{Colors.RESET}  View cybersecurity logs")
    print(f"  {Colors.BOLD}4️⃣{Colors.RESET}  View AI analysis logs")
    print(f"  {Colors.BOLD}5️⃣{Colors.RESET}  Exit")
    print()
    print(Colors.CYAN + "=" * 80 + Colors.RESET)
    print()

def option_1_operator_command():
    """Option 1: Operator Command Panel"""
    print_header()
    print(f"{Colors.YELLOW}{Colors.BOLD}OPERATOR COMMAND PANEL{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    
    print(f"{Colors.GREEN}Enter command parameters (or 'back' to return):{Colors.RESET}")
    print()
    
    # Get breaker status
    breaker = input(f"  Breaker (ON/OFF): ").strip().upper()
    if breaker.lower() == 'back':
        return
    
    if breaker not in ['ON', 'OFF']:
        print(f"{Colors.RED}Invalid breaker state. Must be ON or OFF.{Colors.RESET}")
        input("\nPress Enter to continue...")
        return
    
    # Get voltage
    try:
        voltage_input = input(f"  Voltage (p.u., 0.90-1.10): ").strip()
        if voltage_input.lower() == 'back':
            return
        voltage = float(voltage_input)
        
        # Client-side validation: Voltage Range
        if not (0.90 <= voltage <= 1.10):
            print(f"{Colors.RED}ERROR: Voltage out of permitted range (0.90 - 1.10 p.u.){Colors.RESET}")
            input("\nPress Enter to continue...")
            return
            
    except ValueError:
        print(f"{Colors.RED}Invalid voltage value.{Colors.RESET}")
        input("\nPress Enter to continue...")
        return
    
    # Get frequency
    try:
        frequency_input = input(f"  Frequency (Hz, 49.0-51.0): ").strip()
        if frequency_input.lower() == 'back':
            return
        frequency = float(frequency_input)
        
        # Client-side validation: Frequency Range
        if not (49.0 <= frequency <= 51.0):
            print(f"{Colors.RED}ERROR: Frequency out of permitted range (49.0 - 51.0 Hz){Colors.RESET}")
            input("\nPress Enter to continue...")
            return
            
    except ValueError:
        print(f"{Colors.RED}Invalid frequency value.{Colors.RESET}")
        input("\nPress Enter to continue...")
        return
    
    # Build command
    command = {
        "breaker": breaker,
        "voltage": voltage,
        "frequency": frequency
    }
    
    print()
    print(f"{Colors.YELLOW}Sending command to gateway...{Colors.RESET}")
    print()
    
    # Send to gateway
    try:
        response = requests.post(
            f"{GATEWAY_URL}/operator/command",
            json=command,
            timeout=10
        )
        
        result = response.json()
        
        # Display result
        print(Colors.CYAN + "=" * 80 + Colors.RESET)
        print(f"{Colors.BOLD}GATEWAY RESPONSE{Colors.RESET}")
        print(Colors.CYAN + "=" * 80 + Colors.RESET)
        
        # Status
        status = result.get('status', 'UNKNOWN')
        if status == 'ALLOWED':
            status_color = Colors.GREEN
        elif status == 'BLOCKED':
            status_color = Colors.RED
        else:
            status_color = Colors.YELLOW
        
        print(f"Status:        {status_color}{Colors.BOLD}{status}{Colors.RESET}")
        
        # Only show Risk Score if it's elevated or if blocked
        risk_score = result.get('risk_score', 0)
        if risk_score > 0.3 or status == 'BLOCKED':
            risk_color = Colors.RED if risk_score > 0.7 else Colors.YELLOW
            print(f"Risk Score:    {risk_color}{risk_score:.2f}{Colors.RESET}")
        
        # Only show Attack Type if it's not NORMAL
        attack_type = result.get('attack_type', 'N/A')
        if attack_type not in ['NORMAL', 'N/A', 'None']:
            print(f"Attack Type:   {Colors.MAGENTA}{attack_type}{Colors.RESET}")
        
        # AI Analysis
        if 'ai_analysis' in result:
            ai = result['ai_analysis']
            print()
            print(f"{Colors.CYAN}AI Analysis:{Colors.RESET}")
            print(f"  Decision:    {Colors.BOLD}{ai.get('decision', 'N/A')}{Colors.RESET}")
            print(f"  AI Risk:     {Colors.YELLOW}{ai.get('risk_score', 0):.2f}{Colors.RESET}")
            print(f"  Confidence:  {ai.get('confidence', 0):.2f}")
            print(f"  Explanation: {ai.get('explanation', 'N/A')}")
        
        # Reason (if blocked)
        if 'reason' in result:
            print()
            print(f"{Colors.RED}Reason: {result['reason']}{Colors.RESET}")
        
        # Grid response (if allowed)
        if 'grid_response' in result:
            grid = result['grid_response'].get('grid_state', {})
            print()
            print(f"{Colors.GREEN}Grid Updated:{Colors.RESET}")
            print(f"  Voltage:     {grid.get('voltage', 0):.2f} p.u.")
            print(f"  Frequency:   {grid.get('frequency', 0):.1f} Hz")
            print(f"  Breaker:     {grid.get('breaker', 'N/A')}")
            print(f"  Power Flow:  {grid.get('power_flow', 0):.2f} MW")
        
        print(Colors.CYAN + "=" * 80 + Colors.RESET)
        
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}ERROR: Cannot connect to gateway at {GATEWAY_URL}{Colors.RESET}")
        print(f"{Colors.YELLOW}Make sure the gateway is running on port 5002{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}ERROR: {str(e)}{Colors.RESET}")
    
    print()
    input("Press Enter to continue...")

def option_2_live_monitor():
    """Option 2: Live Grid Monitor"""
    print_header()
    print(f"{Colors.YELLOW}{Colors.BOLD}LIVE GRID MONITOR{Colors.RESET}")
    print(f"{Colors.CYAN}Press Ctrl+C to exit monitor mode{Colors.RESET}")
    print()
    
    try:
        while True:
            # Fetch grid data
            try:
                response = requests.get(f"{GRID_URL}/grid/data", timeout=2)
                data = response.json()
                grid = data.get('grid_state', {})
                
                # Clear and redraw
                print_header()
                print(f"{Colors.YELLOW}{Colors.BOLD}LIVE GRID MONITOR{Colors.RESET}")
                print(f"{Colors.CYAN}Press Ctrl+C to exit monitor mode{Colors.RESET}")
                print()
                print(Colors.CYAN + "=" * 80 + Colors.RESET)
                print(f"{Colors.BOLD}REAL-TIME GRID TELEMETRY{Colors.RESET}")
                print(Colors.CYAN + "=" * 80 + Colors.RESET)
                print()
                
                # Display telemetry
                voltage = grid.get('voltage', 0)
                frequency = grid.get('frequency', 0)
                breaker = grid.get('breaker', 'OFF')
                power = grid.get('power_flow', 0)
                
                # Color code based on status
                voltage_color = Colors.GREEN if 0.95 <= voltage <= 1.05 else Colors.YELLOW
                freq_color = Colors.GREEN if 49.5 <= frequency <= 50.5 else Colors.YELLOW
                breaker_color = Colors.GREEN if breaker == 'ON' else Colors.RED
                
                print(f"  Voltage:       {voltage_color}{voltage:.3f} p.u.{Colors.RESET}")
                print(f"  Frequency:     {freq_color}{frequency:.2f} Hz{Colors.RESET}")
                print(f"  Breaker:       {breaker_color}{Colors.BOLD}{breaker}{Colors.RESET}")
                print(f"  Power Flow:    {Colors.CYAN}{power:.2f} MW{Colors.RESET}")
                print()
                print(f"  Last Update:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                print(Colors.CYAN + "=" * 80 + Colors.RESET)
                
            except requests.exceptions.ConnectionError:
                print(f"{Colors.RED}ERROR: Cannot connect to grid at {GRID_URL}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}ERROR: {str(e)}{Colors.RESET}")
            
            # Wait 1 second
            time.sleep(1)
            
    except KeyboardInterrupt:
        print()
        print(f"{Colors.YELLOW}Exiting monitor mode...{Colors.RESET}")
        time.sleep(1)

def option_3_cyber_logs():
    """Option 3: Cybersecurity Logs Viewer"""
    print_header()
    print(f"{Colors.YELLOW}{Colors.BOLD}CYBERSECURITY LOGS{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    
    if not os.path.exists(CYBER_LOG_PATH):
        print(f"{Colors.YELLOW}No logs found at {CYBER_LOG_PATH}{Colors.RESET}")
        print(f"{Colors.YELLOW}Logs will be created when gateway processes commands.{Colors.RESET}")
    else:
        try:
            with open(CYBER_LOG_PATH, 'r') as f:
                lines = f.readlines()
            
            # Show last 50 lines
            display_lines = lines[-50:] if len(lines) > 50 else lines
            
            print(f"{Colors.GREEN}Showing last {len(display_lines)} log entries:{Colors.RESET}")
            print()
            
            for line in display_lines:
                # Highlight BLOCKED events
                if 'BLOCKED' in line:
                    print(f"{Colors.RED}{line.strip()}{Colors.RESET}")
                elif 'WARNING' in line:
                    print(f"{Colors.YELLOW}{line.strip()}{Colors.RESET}")
                elif 'CRITICAL' in line:
                    print(f"{Colors.RED}{Colors.BOLD}{line.strip()}{Colors.RESET}")
                else:
                    print(line.strip())
            
        except Exception as e:
            print(f"{Colors.RED}ERROR reading log file: {str(e)}{Colors.RESET}")
    
    print()
    input("Press Enter to continue...")

def option_4_ai_logs():
    """Option 4: AI Logs Viewer"""
    print_header()
    print(f"{Colors.YELLOW}{Colors.BOLD}AI ANALYSIS LOGS{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    
    if not os.path.exists(AI_LOG_PATH):
        print(f"{Colors.YELLOW}No logs found at {AI_LOG_PATH}{Colors.RESET}")
        print(f"{Colors.YELLOW}Logs will be created when AI engine analyzes commands.{Colors.RESET}")
    else:
        try:
            with open(AI_LOG_PATH, 'r') as f:
                lines = f.readlines()
            
            # Show last 50 lines
            display_lines = lines[-50:] if len(lines) > 50 else lines
            
            print(f"{Colors.GREEN}Showing last {len(display_lines)} log entries:{Colors.RESET}")
            print()
            
            for line in display_lines:
                # Highlight CRITICAL decisions
                if 'CRITICAL' in line:
                    print(f"{Colors.RED}{Colors.BOLD}{line.strip()}{Colors.RESET}")
                elif 'WARNING' in line:
                    print(f"{Colors.YELLOW}{line.strip()}{Colors.RESET}")
                elif 'AI RISK' in line:
                    print(f"{Colors.MAGENTA}{line.strip()}{Colors.RESET}")
                else:
                    print(line.strip())
            
        except Exception as e:
            print(f"{Colors.RED}ERROR reading log file: {str(e)}{Colors.RESET}")
    
    print()
    input("Press Enter to continue...")

def main():
    """Main application loop"""
    while True:
        print_menu()
        
        choice = input(f"{Colors.GREEN}Select option (1-5): {Colors.RESET}").strip()
        
        if choice == '1':
            option_1_operator_command()
        elif choice == '2':
            option_2_live_monitor()
        elif choice == '3':
            option_3_cyber_logs()
        elif choice == '4':
            option_4_ai_logs()
        elif choice == '5':
            print()
            print(f"{Colors.YELLOW}Shutting down admin console...{Colors.RESET}")
            print(f"{Colors.GREEN}Thank you for using GRID-SHIELD AI!{Colors.RESET}")
            print()
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid option. Please select 1-5.{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"{Colors.YELLOW}Admin console interrupted by user.{Colors.RESET}")
        print(f"{Colors.GREEN}Goodbye!{Colors.RESET}")
        print()
        sys.exit(0)
