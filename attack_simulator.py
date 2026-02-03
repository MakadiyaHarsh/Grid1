#!/usr/bin/env python3
"""
GRID-SHIELD AI Attack Simulator
================================
Cyber attack simulation terminal for demonstrating security capabilities.

Features:
- Multiple attack types (FDIA, Replay, DoS, Injection, etc.)
- Real-time attack execution
- Visual feedback and results
- Pre-configured demo scenarios
"""

import requests
import time
import os
import sys
import json
import random
from datetime import datetime
from threading import Thread

# Configuration
GATEWAY_URL = "http://localhost:5002"
ATTACK_DELAY = 0.5  # Delay between attacks in seconds

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
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Print application header"""
    clear_screen()
    print(Colors.RED + "=" * 80 + Colors.RESET)
    print(Colors.BOLD + Colors.RED + "   ⚠️  GRID-SHIELD AI ATTACK SIMULATOR  ⚠️" + Colors.RESET)
    print(Colors.RED + "=" * 80 + Colors.RESET)
    print(f"{Colors.YELLOW}WARNING: For authorized security testing and demonstrations only{Colors.RESET}")
    print(Colors.RED + "=" * 80 + Colors.RESET)
    print()

def print_menu():
    """Print main menu"""
    print_header()
    print(f"{Colors.CYAN}Attack Types:{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}1️⃣{Colors.RESET}  FDIA Attack (False Data Injection)")
    print(f"  {Colors.BOLD}2️⃣{Colors.RESET}  Replay Attack (Command Repetition)")
    print(f"  {Colors.BOLD}3️⃣{Colors.RESET}  Data Manipulation Attack")
    print(f"  {Colors.BOLD}4️⃣{Colors.RESET}  Parameter Injection Attack")
    print(f"  {Colors.BOLD}5️⃣{Colors.RESET}  Correlation Attack")
    print(f"  {Colors.BOLD}6️⃣{Colors.RESET}  DoS/Flooding Attack")
    print(f"  {Colors.BOLD}7️⃣{Colors.RESET}  Spoofing Attack")
    print(f"  {Colors.BOLD}8️⃣{Colors.RESET}  Multi-Vector Attack")
    print()
    print(f"{Colors.MAGENTA}Demo Scenarios:{Colors.RESET}")
    print(f"  {Colors.BOLD}9️⃣{Colors.RESET}  Investor Demo (Automated)")
    print()
    print(f"  {Colors.BOLD}0️⃣{Colors.RESET}  Exit")
    print()
    print(Colors.RED + "=" * 80 + Colors.RESET)
    print()

def send_attack(command, attack_name):
    """Send attack command to gateway"""
    try:
        response = requests.post(
            f"{GATEWAY_URL}/operator/command",
            json=command,
            timeout=5
        )
        result = response.json()
        
        status = result.get('status', 'UNKNOWN')
        risk_score = result.get('risk_score', 0)
        attack_type = result.get('attack_type', 'N/A')
        
        return {
            'success': True,
            'status': status,
            'risk_score': risk_score,
            'attack_type': attack_type,
            'blocked': status == 'BLOCKED',
            'result': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def display_attack_result(attack_name, result, command):
    """Display attack result"""
    print(f"\n{Colors.CYAN}Attack:{Colors.RESET} {Colors.BOLD}{attack_name}{Colors.RESET}")
    print(f"{Colors.CYAN}Payload:{Colors.RESET} {json.dumps(command, indent=2)}")
    print()
    
    if not result['success']:
        print(f"{Colors.RED}❌ Attack Failed: {result['error']}{Colors.RESET}")
        return
    
    if result['blocked']:
        print(f"{Colors.RED}{Colors.BOLD}🛡️  ATTACK BLOCKED BY GATEWAY{Colors.RESET}")
        print(f"{Colors.YELLOW}Risk Score: {result['risk_score']:.2f}{Colors.RESET}")
        print(f"{Colors.YELLOW}Detected As: {result['attack_type']}{Colors.RESET}")
        
        if 'result' in result and 'reason' in result['result']:
            print(f"{Colors.RED}Reason: {result['result']['reason']}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}✅ Attack Bypassed Security (Command Allowed){Colors.RESET}")
        print(f"{Colors.YELLOW}Risk Score: {result['risk_score']:.2f}{Colors.RESET}")

def attack_1_fdia():
    """FDIA Attack - False Data Injection"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 1: FALSE DATA INJECTION ATTACK (FDIA){Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Coordinated false data that maintains power flow equations")
    print("  Bypasses traditional residual-based detection")
    print("  AI detects through correlation analysis")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    # FDIA payload: High voltage with low frequency (correlation violation)
    attack_payload = {
        "breaker": "ON",
        "voltage": 1.08,
        "frequency": 49.2
    }
    
    print(f"\n{Colors.RED}🚀 Launching FDIA Attack...{Colors.RESET}\n")
    time.sleep(1)
    
    result = send_attack(attack_payload, "FDIA Attack")
    display_attack_result("FDIA Attack", result, attack_payload)
    
    print()
    input("Press Enter to continue...")

def attack_2_replay():
    """Replay Attack - Rapid Command Repetition"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 2: REPLAY ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Rapid repetition of identical commands")
    print("  Detected by command history analysis")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    # Replay payload
    attack_payload = {
        "breaker": "ON",
        "voltage": 1.00,
        "frequency": 50.0
    }
    
    print(f"\n{Colors.RED}🚀 Launching Replay Attack (5 identical commands)...{Colors.RESET}\n")
    
    for i in range(5):
        print(f"{Colors.YELLOW}Attempt {i+1}/5...{Colors.RESET}")
        result = send_attack(attack_payload, f"Replay Attack #{i+1}")
        
        if result['blocked']:
            print(f"{Colors.RED}  → BLOCKED{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}  → Allowed{Colors.RESET}")
        
        time.sleep(ATTACK_DELAY)
    
    print()
    input("Press Enter to continue...")

def attack_3_data_manipulation():
    """Data Manipulation Attack - Abnormal Spikes"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 3: DATA MANIPULATION ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Sudden abnormal parameter changes")
    print("  Detected by spike analysis")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    # Send normal command first
    normal_payload = {
        "breaker": "ON",
        "voltage": 1.00,
        "frequency": 50.0
    }
    
    print(f"\n{Colors.CYAN}Step 1: Sending normal command...{Colors.RESET}")
    send_attack(normal_payload, "Normal Command")
    time.sleep(1)
    
    # Then send abnormal spike
    spike_payload = {
        "breaker": "ON",
        "voltage": 1.09,  # Sudden spike
        "frequency": 50.8  # Sudden spike
    }
    
    print(f"\n{Colors.RED}🚀 Step 2: Launching Data Manipulation (Abnormal Spike)...{Colors.RESET}\n")
    time.sleep(1)
    
    result = send_attack(spike_payload, "Data Manipulation Attack")
    display_attack_result("Data Manipulation Attack", result, spike_payload)
    
    print()
    input("Press Enter to continue...")

def attack_4_parameter_injection():
    """Parameter Injection Attack - Out of Range Values"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 4: PARAMETER INJECTION ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Injecting out-of-range parameter values")
    print("  Detected by cyber rules validation")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    # Out of range payload
    attack_payload = {
        "breaker": "ON",
        "voltage": 1.25,  # Way out of range (0.90-1.10)
        "frequency": 52.5  # Way out of range (49.0-51.0)
    }
    
    print(f"\n{Colors.RED}🚀 Launching Parameter Injection Attack...{Colors.RESET}\n")
    time.sleep(1)
    
    result = send_attack(attack_payload, "Parameter Injection Attack")
    display_attack_result("Parameter Injection Attack", result, attack_payload)
    
    print()
    input("Press Enter to continue...")

def attack_5_correlation():
    """Correlation Attack - Inconsistent Parameters"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 5: CORRELATION ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Breaker OFF with high voltage/frequency")
    print("  Detected by correlation anomaly analysis")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    # Inconsistent payload
    attack_payload = {
        "breaker": "OFF",  # Breaker off
        "voltage": 1.08,   # But high voltage
        "frequency": 50.6  # And high frequency
    }
    
    print(f"\n{Colors.RED}🚀 Launching Correlation Attack...{Colors.RESET}\n")
    time.sleep(1)
    
    result = send_attack(attack_payload, "Correlation Attack")
    display_attack_result("Correlation Attack", result, attack_payload)
    
    print()
    input("Press Enter to continue...")

def attack_6_dos_flooding():
    """DoS/Flooding Attack - Rapid Command Flooding"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 6: DoS/FLOODING ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Rapid flooding of commands to overwhelm system")
    print("  Detected by rate limiting and pattern analysis")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    print(f"\n{Colors.RED}🚀 Launching DoS Flooding Attack (20 rapid commands)...{Colors.RESET}\n")
    
    blocked_count = 0
    allowed_count = 0
    
    for i in range(20):
        # Random payloads to avoid simple replay detection
        attack_payload = {
            "breaker": random.choice(["ON", "OFF"]),
            "voltage": round(random.uniform(0.95, 1.05), 2),
            "frequency": round(random.uniform(49.5, 50.5), 1)
        }
        
        result = send_attack(attack_payload, f"Flood #{i+1}")
        
        if result['success']:
            if result['blocked']:
                blocked_count += 1
                print(f"{Colors.RED}#{i+1:02d} BLOCKED{Colors.RESET}", end=" ")
            else:
                allowed_count += 1
                print(f"{Colors.GREEN}#{i+1:02d} Allowed{Colors.RESET}", end=" ")
        
        if (i + 1) % 5 == 0:
            print()
        
        time.sleep(0.1)  # Very rapid
    
    print()
    print()
    print(f"{Colors.CYAN}Results:{Colors.RESET}")
    print(f"  Blocked: {Colors.RED}{blocked_count}{Colors.RESET}")
    print(f"  Allowed: {Colors.GREEN}{allowed_count}{Colors.RESET}")
    
    print()
    input("Press Enter to continue...")

def attack_7_spoofing():
    """Spoofing Attack - Fake Operator Commands"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 7: SPOOFING ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Simulating commands from unauthorized source")
    print("  Testing authentication and authorization")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    # Spoofed payload with suspicious patterns
    attack_payload = {
        "breaker": "ON",
        "voltage": 0.91,  # At boundary
        "frequency": 51.0  # At boundary
    }
    
    print(f"\n{Colors.RED}🚀 Launching Spoofing Attack...{Colors.RESET}\n")
    time.sleep(1)
    
    result = send_attack(attack_payload, "Spoofing Attack")
    display_attack_result("Spoofing Attack", result, attack_payload)
    
    print()
    input("Press Enter to continue...")

def attack_8_multi_vector():
    """Multi-Vector Attack - Combined Attack Types"""
    print_header()
    print(f"{Colors.RED}{Colors.BOLD}ATTACK TYPE 8: MULTI-VECTOR ATTACK{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}Description:{Colors.RESET}")
    print("  Combination of multiple attack techniques")
    print("  Tests comprehensive defense capabilities")
    print()
    
    input(f"{Colors.GREEN}Press Enter to launch attack...{Colors.RESET}")
    
    attacks = [
        ("FDIA", {"breaker": "ON", "voltage": 1.09, "frequency": 49.1}),
        ("Injection", {"breaker": "ON", "voltage": 1.11, "frequency": 51.2}),
        ("Correlation", {"breaker": "OFF", "voltage": 1.07, "frequency": 50.7}),
        ("Replay", {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}),
        ("Replay", {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}),
    ]
    
    print(f"\n{Colors.RED}🚀 Launching Multi-Vector Attack (5 attack types)...{Colors.RESET}\n")
    
    for i, (attack_type, payload) in enumerate(attacks, 1):
        print(f"{Colors.YELLOW}Vector {i}/5: {attack_type}{Colors.RESET}")
        result = send_attack(payload, attack_type)
        
        if result['success']:
            if result['blocked']:
                print(f"  {Colors.RED}→ BLOCKED (Risk: {result['risk_score']:.2f}){Colors.RESET}")
            else:
                print(f"  {Colors.GREEN}→ Allowed{Colors.RESET}")
        
        time.sleep(ATTACK_DELAY)
    
    print()
    input("Press Enter to continue...")

def demo_scenario_investor():
    """Automated Investor Demo Scenario"""
    print_header()
    print(f"{Colors.MAGENTA}{Colors.BOLD}INVESTOR DEMO SCENARIO{Colors.RESET}")
    print(Colors.CYAN + "-" * 80 + Colors.RESET)
    print()
    print(f"{Colors.YELLOW}This automated demo will showcase:{Colors.RESET}")
    print("  1. Normal operation (command allowed)")
    print("  2. FDIA attack (AI detection)")
    print("  3. Replay attack (traditional detection)")
    print("  4. Multi-vector attack (comprehensive defense)")
    print()
    
    input(f"{Colors.GREEN}Press Enter to start automated demo...{Colors.RESET}")
    
    scenarios = [
        ("Normal Operation", {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}),
        ("FDIA Attack", {"breaker": "ON", "voltage": 1.08, "frequency": 49.2}),
        ("Replay Attack #1", {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}),
        ("Replay Attack #2", {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}),
        ("Replay Attack #3", {"breaker": "ON", "voltage": 1.00, "frequency": 50.0}),
        ("Parameter Injection", {"breaker": "ON", "voltage": 1.12, "frequency": 51.5}),
    ]
    
    for i, (scenario_name, payload) in enumerate(scenarios, 1):
        print()
        print(Colors.CYAN + "=" * 80 + Colors.RESET)
        print(f"{Colors.BOLD}Scenario {i}/{len(scenarios)}: {scenario_name}{Colors.RESET}")
        print(Colors.CYAN + "=" * 80 + Colors.RESET)
        print()
        
        result = send_attack(payload, scenario_name)
        display_attack_result(scenario_name, result, payload)
        
        time.sleep(2)
    
    print()
    print(Colors.GREEN + "=" * 80 + Colors.RESET)
    print(f"{Colors.GREEN}{Colors.BOLD}✅ INVESTOR DEMO COMPLETE{Colors.RESET}")
    print(Colors.GREEN + "=" * 80 + Colors.RESET)
    print()
    input("Press Enter to continue...")

def main():
    """Main application loop"""
    while True:
        print_menu()
        
        choice = input(f"{Colors.RED}Select attack type (0-9): {Colors.RESET}").strip()
        
        if choice == '1':
            attack_1_fdia()
        elif choice == '2':
            attack_2_replay()
        elif choice == '3':
            attack_3_data_manipulation()
        elif choice == '4':
            attack_4_parameter_injection()
        elif choice == '5':
            attack_5_correlation()
        elif choice == '6':
            attack_6_dos_flooding()
        elif choice == '7':
            attack_7_spoofing()
        elif choice == '8':
            attack_8_multi_vector()
        elif choice == '9':
            demo_scenario_investor()
        elif choice == '0':
            print()
            print(f"{Colors.YELLOW}Shutting down attack simulator...{Colors.RESET}")
            print(f"{Colors.GREEN}Stay secure!{Colors.RESET}")
            print()
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid option. Please select 0-9.{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"{Colors.YELLOW}Attack simulator interrupted by user.{Colors.RESET}")
        print(f"{Colors.GREEN}Goodbye!{Colors.RESET}")
        print()
        sys.exit(0)
