"""
Security Event Logger
Structured logging for cybersecurity events with terminal output
"""

import datetime
import os
from typing import Dict, Any, Optional

class SecurityLogger:
    """Handles structured security event logging"""
    
    # ANSI color codes for terminal output
    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'BOLD': '\033[1m',
    }
    
    def __init__(self, enable_color: bool = True):
        self.enable_color = enable_color
        
        # Setup file logging
        self.log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'cyber.log')
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled"""
        if not self.enable_color:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['RESET']}"
    
    def log_event(
        self,
        request_id: str,
        source: str,
        command: Dict[str, Any],
        decision: str,
        attack_type: str,
        risk_score: float,
        reason: Optional[str] = None,
        grid_response: Optional[Dict] = None
    ):
        """Log a complete security event"""
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {decision} — {attack_type} (Risk: {risk_score:.2f})\n")
            if reason:
                f.write(f"[{timestamp}] REASON: {reason}\n")
        
        # Determine color based on decision
        if decision == "BLOCKED":
            header_color = 'RED'
            decision_color = 'RED'
        elif decision == "ALLOWED":
            header_color = 'GREEN'
            decision_color = 'GREEN'
        else:
            header_color = 'YELLOW'
            decision_color = 'YELLOW'
        
        # Build log output
        separator = "=" * 80
        print()
        print(self._colorize(separator, header_color))
        print(self._colorize("CYBERSECURITY EVENT", 'BOLD'))
        print(self._colorize(separator, header_color))
        print(f"{self._colorize('Timestamp:', 'CYAN')}      {timestamp}")
        print(f"{self._colorize('Request ID:', 'CYAN')}     {request_id}")
        print(f"{self._colorize('Source:', 'CYAN')}         {source}")
        print(f"{self._colorize('Command:', 'CYAN')}        {command}")
        print(f"{self._colorize('Decision:', 'CYAN')}       {self._colorize(decision, decision_color)}")
        print(f"{self._colorize('Attack Type:', 'CYAN')}    {self._colorize(attack_type, 'MAGENTA')}")
        print(f"{self._colorize('Risk Score:', 'CYAN')}     {self._colorize(f'{risk_score:.2f}', 'YELLOW')}")
        
        if reason:
            print(f"{self._colorize('Reason:', 'CYAN')}         {reason}")
        
        if grid_response:
            print(f"{self._colorize('Grid Response:', 'CYAN')}  {grid_response}")
        
        print(self._colorize(separator, header_color))
        print()
    
    def log_info(self, message: str):
        """Log informational message"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] INFO: {message}\n")
        print(f"{self._colorize('[INFO]', 'BLUE')} {timestamp} - {message}")
    
    def log_warning(self, message: str):
        """Log warning message"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] WARNING: {message}\n")
        print(f"{self._colorize('[WARNING]', 'YELLOW')} {timestamp} - {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] ERROR: {message}\n")
        print(f"{self._colorize('[ERROR]', 'RED')} {timestamp} - {message}")
    
    def log_critical(self, message: str):
        """Log critical message"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{self._colorize('[CRITICAL]', 'RED') + self._colorize('[BOLD]', 'BOLD')} {timestamp} - {message}")
