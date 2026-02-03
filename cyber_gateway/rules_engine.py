"""
Cyber Rules Engine
Rule-based cybersecurity validation for power grid commands
"""

from typing import Dict, Any, List, Tuple
import config

class CyberRulesEngine:
    """Validates commands against cybersecurity rules"""
    
    def __init__(self):
        self.required_parameters = ["breaker", "voltage", "frequency"]
    
    def validate_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate command against all cyber rules
        
        Returns:
            {
                "status": "ALLOWED" | "BLOCKED",
                "reason": str,
                "risk_level": float (0.0 - 1.0),
                "violations": list
            }
        """
        violations = []
        risk_level = 0.0
        
        # Check for missing parameters
        missing_params = self._check_missing_parameters(command)
        if missing_params:
            violations.append(f"Missing required parameters: {', '.join(missing_params)}")
            risk_level = max(risk_level, 0.9)
        
        # Check voltage range
        voltage_violation = self._check_voltage(command.get("voltage"))
        if voltage_violation:
            violations.append(voltage_violation)
            risk_level = max(risk_level, 0.8)
        
        # Check frequency range
        frequency_violation = self._check_frequency(command.get("frequency"))
        if frequency_violation:
            violations.append(frequency_violation)
            risk_level = max(risk_level, 0.8)
        
        # Check breaker state
        breaker_violation = self._check_breaker(command.get("breaker"))
        if breaker_violation:
            violations.append(breaker_violation)
            risk_level = max(risk_level, 0.7)
        
        # Check data types
        type_violation = self._check_data_types(command)
        if type_violation:
            violations.append(type_violation)
            risk_level = max(risk_level, 0.85)
        
        # Determine status
        if violations:
            status = "BLOCKED"
            reason = "; ".join(violations)
        else:
            status = "ALLOWED"
            reason = "All cyber rules passed"
            risk_level = 0.1  # Minimal risk for valid commands
        
        return {
            "status": status,
            "reason": reason,
            "risk_level": risk_level,
            "violations": violations
        }
    
    def _check_missing_parameters(self, command: Dict[str, Any]) -> List[str]:
        """Check for missing required parameters"""
        missing = []
        for param in self.required_parameters:
            if param not in command:
                missing.append(param)
        return missing
    
    def _check_voltage(self, voltage: Any) -> str:
        """Validate voltage range"""
        if voltage is None:
            return ""  # Will be caught by missing parameter check
        
        try:
            voltage_val = float(voltage)
            if voltage_val < config.VOLTAGE_MIN or voltage_val > config.VOLTAGE_MAX:
                return f"Voltage {voltage_val} pu outside safe range [{config.VOLTAGE_MIN}, {config.VOLTAGE_MAX}] pu"
        except (ValueError, TypeError):
            return f"Invalid voltage value: {voltage}"
        
        return ""
    
    def _check_frequency(self, frequency: Any) -> str:
        """Validate frequency range"""
        if frequency is None:
            return ""  # Will be caught by missing parameter check
        
        try:
            freq_val = float(frequency)
            if freq_val < config.FREQUENCY_MIN or freq_val > config.FREQUENCY_MAX:
                return f"Frequency {freq_val} Hz outside safe range [{config.FREQUENCY_MIN}, {config.FREQUENCY_MAX}] Hz"
        except (ValueError, TypeError):
            return f"Invalid frequency value: {frequency}"
        
        return ""
    
    def _check_breaker(self, breaker: Any) -> str:
        """Validate breaker state"""
        if breaker is None:
            return ""  # Will be caught by missing parameter check
        
        if not isinstance(breaker, str):
            return f"Invalid breaker type: expected string, got {type(breaker).__name__}"
        
        if breaker not in config.VALID_BREAKER_STATES:
            return f"Invalid breaker state '{breaker}'. Must be one of: {', '.join(config.VALID_BREAKER_STATES)}"
        
        return ""
    
    def _check_data_types(self, command: Dict[str, Any]) -> str:
        """Validate data types of parameters"""
        errors = []
        
        # Check voltage is numeric
        if "voltage" in command:
            try:
                float(command["voltage"])
            except (ValueError, TypeError):
                errors.append(f"voltage must be numeric")
        
        # Check frequency is numeric
        if "frequency" in command:
            try:
                float(command["frequency"])
            except (ValueError, TypeError):
                errors.append(f"frequency must be numeric")
        
        # Check breaker is string
        if "breaker" in command and not isinstance(command["breaker"], str):
            errors.append(f"breaker must be string")
        
        if errors:
            return "Data type violations: " + ", ".join(errors)
        
        return ""
