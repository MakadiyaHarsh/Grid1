"""
Attack Detection Module
Cyber attack detection algorithms for power grid security
"""

from typing import Dict, Any, List
import datetime
import config

class AttackDetector:
    """Detects cyber attacks on power grid commands"""
    
    def __init__(self):
        self.command_history: List[Dict[str, Any]] = []
    
    def analyze_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze command for cyber attack patterns
        
        Returns:
            {
                "attack_type": str,
                "anomaly_score": float (0.0 - 1.0),
                "details": str
            }
        """
        anomaly_score = 0.0
        attack_types = []
        details = []
        
        # Check for False Data Injection Attack (FDIA)
        fdia_score, fdia_detail = self._detect_fdia(command)
        if fdia_score > 0:
            anomaly_score = max(anomaly_score, fdia_score)
            attack_types.append("FDIA_SUSPECTED")
            details.append(fdia_detail)
        
        # Check for Data Manipulation
        manipulation_score, manip_detail = self._detect_data_manipulation(command)
        if manipulation_score > 0:
            anomaly_score = max(anomaly_score, manipulation_score)
            attack_types.append("DATA_MANIPULATION")
            details.append(manip_detail)
        
        # Check for Replay Attack
        replay_score, replay_detail = self._detect_replay_attack(command)
        if replay_score > 0:
            anomaly_score = max(anomaly_score, replay_score)
            attack_types.append("REPLAY_ATTACK")
            details.append(replay_detail)
        
        # Check for Parameter Correlation Anomalies
        correlation_score, corr_detail = self._detect_correlation_anomaly(command)
        if correlation_score > 0:
            anomaly_score = max(anomaly_score, correlation_score)
            details.append(corr_detail)
        
        # Store command in history
        self._add_to_history(command)
        
        # Determine primary attack type
        if attack_types:
            attack_type = attack_types[0]  # Primary attack type
        else:
            attack_type = "NORMAL"
        
        return {
            "attack_type": attack_type,
            "anomaly_score": anomaly_score,
            "details": " | ".join(details) if details else "No anomalies detected"
        }
    
    def _detect_fdia(self, command: Dict[str, Any]) -> tuple:
        """Detect False Data Injection Attack patterns"""
        score = 0.0
        detail = ""
        
        try:
            voltage = float(command.get("voltage", 1.0))
            frequency = float(command.get("frequency", 50.0))
            
            # Check for values at extreme boundaries (common FDIA pattern)
            voltage_at_boundary = (
                abs(voltage - config.VOLTAGE_MIN) < 0.01 or 
                abs(voltage - config.VOLTAGE_MAX) < 0.01
            )
            frequency_at_boundary = (
                abs(frequency - config.FREQUENCY_MIN) < 0.1 or 
                abs(frequency - config.FREQUENCY_MAX) < 0.1
            )
            
            if voltage_at_boundary and frequency_at_boundary:
                score = 0.85
                detail = "Both voltage and frequency at extreme boundaries - FDIA pattern"
            elif voltage_at_boundary or frequency_at_boundary:
                score = 0.65
                detail = "Parameter at extreme boundary - possible FDIA"
            
            # Check for unrealistic combinations
            # High voltage with high frequency is suspicious
            if voltage > 1.08 and frequency > 50.5:
                score = max(score, 0.75)
                detail = "Unrealistic high voltage-frequency combination"
            
            # Low voltage with low frequency is also suspicious
            if voltage < 0.92 and frequency < 49.5:
                score = max(score, 0.75)
                detail = "Unrealistic low voltage-frequency combination"
                
        except (ValueError, TypeError):
            pass
        
        return score, detail
    
    def _detect_data_manipulation(self, command: Dict[str, Any]) -> tuple:
        """Detect abnormal value spikes or sudden changes"""
        score = 0.0
        detail = ""
        
        if len(self.command_history) == 0:
            return 0.0, ""
        
        try:
            current_voltage = float(command.get("voltage", 1.0))
            current_frequency = float(command.get("frequency", 50.0))
            
            # Get last command
            last_cmd = self.command_history[-1]
            last_voltage = float(last_cmd.get("voltage", 1.0))
            last_frequency = float(last_cmd.get("frequency", 50.0))
            
            # Calculate changes
            voltage_change = abs(current_voltage - last_voltage)
            frequency_change = abs(current_frequency - last_frequency)
            
            # Detect abnormal spikes
            # Voltage shouldn't change more than 0.15 pu suddenly
            if voltage_change > 0.15:
                score = max(score, 0.70)
                detail = f"Abnormal voltage spike: {voltage_change:.3f} pu change"
            
            # Frequency shouldn't change more than 1.0 Hz suddenly
            if frequency_change > 1.0:
                score = max(score, 0.70)
                detail = f"Abnormal frequency spike: {frequency_change:.2f} Hz change"
            
            # Both changing significantly is very suspicious
            if voltage_change > 0.10 and frequency_change > 0.5:
                score = max(score, 0.80)
                detail = "Simultaneous abnormal changes in multiple parameters"
                
        except (ValueError, TypeError):
            pass
        
        return score, detail
    
    def _detect_replay_attack(self, command: Dict[str, Any]) -> tuple:
        """Detect rapid command repetition patterns"""
        score = 0.0
        detail = ""
        
        if len(self.command_history) < 2:
            return 0.0, ""
        
        # Check recent history for identical commands
        current_time = datetime.datetime.now()
        identical_count = 0
        
        for hist_cmd in reversed(self.command_history[-10:]):  # Check last 10 commands
            # Check if command is identical
            if (hist_cmd.get("breaker") == command.get("breaker") and
                hist_cmd.get("voltage") == command.get("voltage") and
                hist_cmd.get("frequency") == command.get("frequency")):
                
                # Check if within time window
                time_diff = (current_time - hist_cmd.get("timestamp", current_time)).total_seconds()
                if time_diff <= config.REPLAY_WINDOW_SECONDS:
                    identical_count += 1
        
        if identical_count >= config.REPLAY_COUNT_THRESHOLD:
            score = 0.90
            detail = f"Replay attack: {identical_count} identical commands in {config.REPLAY_WINDOW_SECONDS}s window"
        elif identical_count >= 2:
            score = 0.60
            detail = f"Possible replay: {identical_count} identical commands detected"
        
        return score, detail
    
    def _detect_correlation_anomaly(self, command: Dict[str, Any]) -> tuple:
        """Detect inconsistent relationships between parameters"""
        score = 0.0
        detail = ""
        
        try:
            voltage = float(command.get("voltage", 1.0))
            frequency = float(command.get("frequency", 50.0))
            breaker = command.get("breaker", "ON")
            
            # If breaker is OFF, voltage and frequency should be nominal or low
            if breaker == "OFF":
                if voltage > 1.05 or frequency > 50.5:
                    score = 0.65
                    detail = "Inconsistent: Breaker OFF but high voltage/frequency"
            
            # Extreme voltage deviation with normal frequency is suspicious
            voltage_deviation = abs(voltage - 1.0)
            frequency_deviation = abs(frequency - 50.0)
            
            if voltage_deviation > 0.08 and frequency_deviation < 0.2:
                score = max(score, 0.55)
                detail = "Correlation anomaly: Large voltage deviation without frequency impact"
            
            if frequency_deviation > 0.8 and voltage_deviation < 0.03:
                score = max(score, 0.55)
                detail = "Correlation anomaly: Large frequency deviation without voltage impact"
                
        except (ValueError, TypeError):
            pass
        
        return score, detail
    
    def _add_to_history(self, command: Dict[str, Any]):
        """Add command to history with timestamp"""
        command_copy = command.copy()
        command_copy["timestamp"] = datetime.datetime.now()
        
        self.command_history.append(command_copy)
        
        # Maintain history size limit
        if len(self.command_history) > config.MAX_COMMAND_HISTORY:
            self.command_history.pop(0)
