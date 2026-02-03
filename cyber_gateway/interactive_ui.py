#!/usr/bin/env python3
"""
Interactive Terminal UI for Cybersecurity Gateway
Allows users to input commands with a graphical interface
"""

import requests
import json
import sys
import os

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

GATEWAY_URL = "http://localhost:5002/operator/command"

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Print the application header"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     CYBERSECURITY GATEWAY - INTERACTIVE COMMAND INTERFACE     ║")
    print("║              AI-Driven Power Grid Protection                  ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

def print_box(title, content, color=Colors.BLUE):
    """Print a colored box with content"""
    width = 64
    print(f"\n{color}┌{'─' * (width - 2)}┐")
    print(f"│ {Colors.BOLD}{title}{Colors.RESET}{color}{' ' * (width - len(title) - 3)}│")
    print(f"├{'─' * (width - 2)}┤")
    for line in content:
        padding = width - len(line) - 3
        print(f"│ {Colors.RESET}{line}{color}{' ' * padding}│")
    print(f"└{'─' * (width - 2)}┘{Colors.RESET}")

def get_input(prompt, default=None, input_type=str, min_val=None, max_val=None):
    """Get validated input from user"""
    while True:
        try:
            if default is not None:
                user_input = input(f"{Colors.YELLOW}{prompt} [{default}]: {Colors.RESET}").strip()
                if not user_input:
                    return default
            else:
                user_input = input(f"{Colors.YELLOW}{prompt}: {Colors.RESET}").strip()
            
            if input_type == float:
                value = float(user_input)
                if min_val is not None and value < min_val:
                    print(f"{Colors.RED}✗ Value must be >= {min_val}{Colors.RESET}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"{Colors.RED}✗ Value must be <= {max_val}{Colors.RESET}")
                    continue
                return value
            elif input_type == str:
                return user_input.upper()
            else:
                return input_type(user_input)
        except ValueError:
            print(f"{Colors.RED}✗ Invalid input. Please try again.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operation cancelled.{Colors.RESET}")
            return None

def display_valid_ranges():
    """Display valid parameter ranges"""
    ranges = [
        f"{Colors.GREEN}Voltage:{Colors.RESET}    0.90 - 1.10 pu",
        f"{Colors.GREEN}Frequency:{Colors.RESET}  49.0 - 51.0 Hz",
        f"{Colors.GREEN}Breaker:{Colors.RESET}    ON or OFF"
    ]
    print_box("VALID PARAMETER RANGES", ranges, Colors.BLUE)

def display_response(response_data, status_code):
    """Display the gateway response in a formatted way"""
    if status_code == 200:
        # Allowed command
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗")
        print(f"║                    ✓ COMMAND ALLOWED                          ║")
        print(f"╚════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        details = [
            f"Status:       {Colors.GREEN}ALLOWED{Colors.RESET}",
            f"Attack Type:  {response_data.get('attack_type', 'N/A')}",
            f"Risk Score:   {response_data.get('risk_score', 0):.2f}",
            f"Request ID:   {response_data.get('request_id', 'N/A')}"
        ]
        
        if 'grid_response' in response_data:
            grid_state = response_data['grid_response'].get('grid_state', {})
            details.append("")
            details.append(f"{Colors.CYAN}Grid State Updated:{Colors.RESET}")
            details.append(f"  Breaker:    {grid_state.get('breaker', 'N/A')}")
            details.append(f"  Voltage:    {grid_state.get('voltage', 0):.2f} pu")
            details.append(f"  Frequency:  {grid_state.get('frequency', 0):.2f} Hz")
            details.append(f"  Power Flow: {grid_state.get('power_flow', 0):.2f} MW")
        
        print_box("RESPONSE DETAILS", details, Colors.GREEN)
        
    elif status_code == 403:
        # Blocked command
        print(f"\n{Colors.RED}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗")
        print(f"║                    ✗ COMMAND BLOCKED                          ║")
        print(f"╚════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        details = [
            f"Status:       {Colors.RED}BLOCKED{Colors.RESET}",
            f"Attack Type:  {Colors.RED}{response_data.get('attack_type', 'N/A')}{Colors.RESET}",
            f"Risk Score:   {Colors.RED}{response_data.get('risk_score', 0):.2f}{Colors.RESET}",
            f"Request ID:   {response_data.get('request_id', 'N/A')}",
            "",
            f"{Colors.YELLOW}Reason:{Colors.RESET}",
            f"  {response_data.get('reason', 'N/A')}"
        ]
        
        print_box("SECURITY ALERT", details, Colors.RED)
        
    elif status_code == 502:
        # Grid error
        print(f"\n{Colors.YELLOW}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗")
        print(f"║                 ⚠ GRID COMMUNICATION ERROR                    ║")
        print(f"╚════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        details = [
            f"Status:       {Colors.YELLOW}ALLOWED (Security Passed){Colors.RESET}",
            f"Grid Status:  {Colors.RED}UNREACHABLE{Colors.RESET}",
            f"Risk Score:   {response_data.get('risk_score', 0):.2f}",
            "",
            f"{Colors.YELLOW}Note:{Colors.RESET}",
            f"  Command passed security checks but could not reach grid.",
            f"  Ensure grid simulator is running on port 5001."
        ]
        
        print_box("WARNING", details, Colors.YELLOW)

def send_command(breaker, voltage, frequency):
    """Send command to the gateway"""
    command = {
        "breaker": breaker,
        "voltage": voltage,
        "frequency": frequency
    }
    
    print(f"\n{Colors.CYAN}Sending command to gateway...{Colors.RESET}")
    
    try:
        response = requests.post(
            GATEWAY_URL,
            json=command,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        response_data = response.json()
        display_response(response_data, response.status_code)
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}✗ ERROR: Cannot connect to gateway at {GATEWAY_URL}{Colors.RESET}")
        print(f"{Colors.YELLOW}  Make sure the gateway is running on port 5002{Colors.RESET}")
        return False
    except requests.exceptions.Timeout:
        print(f"\n{Colors.RED}✗ ERROR: Request timed out{Colors.RESET}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}✗ ERROR: {str(e)}{Colors.RESET}")
        return False

def main_menu():
    """Display main menu and get user choice"""
    while True:
        clear_screen()
        print_header()
        
        print(f"\n{Colors.BOLD}MAIN MENU{Colors.RESET}")
        print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.RESET}")
        print(f"  {Colors.GREEN}1.{Colors.RESET} Send Custom Command")
        print(f"  {Colors.GREEN}2.{Colors.RESET} Send Preset Commands")
        print(f"  {Colors.GREEN}3.{Colors.RESET} View Valid Ranges")
        print(f"  {Colors.GREEN}4.{Colors.RESET} Check Gateway Health")
        print(f"  {Colors.RED}5.{Colors.RESET} Exit")
        print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.RESET}")
        
        choice = input(f"\n{Colors.YELLOW}Select option [1-5]: {Colors.RESET}").strip()
        
        if choice == '1':
            custom_command_interface()
        elif choice == '2':
            preset_commands_interface()
        elif choice == '3':
            clear_screen()
            print_header()
            display_valid_ranges()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
        elif choice == '4':
            check_health()
        elif choice == '5':
            print(f"\n{Colors.CYAN}Thank you for using GRID-SHIELD AI!{Colors.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid option. Please try again.{Colors.RESET}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

def custom_command_interface():
    """Interface for entering custom commands"""
    clear_screen()
    print_header()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}CUSTOM COMMAND ENTRY{Colors.RESET}")
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.RESET}")
    
    display_valid_ranges()
    
    print(f"\n{Colors.BOLD}Enter Command Parameters:{Colors.RESET}")
    
    # Get breaker state
    breaker = get_input("Breaker State (ON/OFF)", default="ON", input_type=str)
    if breaker is None:
        return
    
    while breaker not in ["ON", "OFF"]:
        print(f"{Colors.RED}✗ Breaker must be ON or OFF{Colors.RESET}")
        breaker = get_input("Breaker State (ON/OFF)", default="ON", input_type=str)
        if breaker is None:
            return
    
    # Get voltage
    voltage = get_input("Voltage (pu)", default=1.0, input_type=float, min_val=0.0, max_val=2.0)
    if voltage is None:
        return
    
    # Get frequency
    frequency = get_input("Frequency (Hz)", default=50.0, input_type=float, min_val=0.0, max_val=100.0)
    if frequency is None:
        return
    
    # Confirm command
    print(f"\n{Colors.BOLD}Command Summary:{Colors.RESET}")
    print(f"  Breaker:   {Colors.CYAN}{breaker}{Colors.RESET}")
    print(f"  Voltage:   {Colors.CYAN}{voltage:.2f} pu{Colors.RESET}")
    print(f"  Frequency: {Colors.CYAN}{frequency:.2f} Hz{Colors.RESET}")
    
    confirm = input(f"\n{Colors.YELLOW}Send this command? (y/n) [y]: {Colors.RESET}").strip().lower()
    
    if confirm in ['', 'y', 'yes']:
        send_command(breaker, voltage, frequency)
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.RESET}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

def preset_commands_interface():
    """Interface for sending preset commands"""
    clear_screen()
    print_header()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}PRESET COMMANDS{Colors.RESET}")
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.RESET}")
    
    presets = [
        ("Normal Operation", "ON", 1.02, 50.1, Colors.GREEN),
        ("Low Voltage", "ON", 0.95, 50.0, Colors.GREEN),
        ("High Voltage", "ON", 1.08, 50.0, Colors.GREEN),
        ("Breaker OFF", "OFF", 0.0, 0.0, Colors.GREEN),
        ("FDIA Attack (Will Block)", "ON", 1.10, 51.0, Colors.RED),
        ("Voltage Violation (Will Block)", "ON", 1.25, 50.0, Colors.RED),
        ("Frequency Violation (Will Block)", "ON", 1.0, 52.5, Colors.RED),
    ]
    
    for i, (name, breaker, voltage, frequency, color) in enumerate(presets, 1):
        print(f"  {color}{i}.{Colors.RESET} {name}")
        print(f"     Breaker: {breaker}, Voltage: {voltage} pu, Frequency: {frequency} Hz")
    
    print(f"  {Colors.YELLOW}0.{Colors.RESET} Back to Main Menu")
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select preset [0-{len(presets)}]: {Colors.RESET}").strip()
    
    try:
        choice_num = int(choice)
        if choice_num == 0:
            return
        elif 1 <= choice_num <= len(presets):
            name, breaker, voltage, frequency, _ = presets[choice_num - 1]
            print(f"\n{Colors.CYAN}Sending: {name}{Colors.RESET}")
            send_command(breaker, voltage, frequency)
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
        else:
            print(f"{Colors.RED}Invalid option.{Colors.RESET}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    except ValueError:
        print(f"{Colors.RED}Invalid input.{Colors.RESET}")
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

def check_health():
    """Check gateway and grid health"""
    clear_screen()
    print_header()
    
    print(f"\n{Colors.CYAN}Checking system health...{Colors.RESET}\n")
    
    try:
        response = requests.get("http://localhost:5002/health", timeout=5)
        health_data = response.json()
        
        gateway_status = health_data.get('gateway', 'unknown')
        grid_status = health_data.get('grid_connection', 'unknown')
        
        details = [
            f"Gateway:         {Colors.GREEN if gateway_status == 'healthy' else Colors.RED}{gateway_status.upper()}{Colors.RESET}",
            f"Grid Connection: {Colors.GREEN if grid_status == 'healthy' else Colors.RED}{grid_status.upper()}{Colors.RESET}",
            f"Timestamp:       {health_data.get('timestamp', 'N/A')}"
        ]
        
        print_box("SYSTEM HEALTH", details, Colors.BLUE)
        
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}✗ Cannot connect to gateway{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {str(e)}{Colors.RESET}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}Thank you for using GRID-SHIELD AI!{Colors.RESET}\n")
        sys.exit(0)
