"""
Physics-Aware Validation Model (MODEL-3)

Purpose:
    Validate cyber data against physical laws of power systems
    
Physical Laws Enforced:
    1. Breaker rule: breaker_status == "OFF" ⇒ power_flow == 0
    2. Causality: voltage must exist before frequency
    3. Power-voltage coupling: power trend must follow voltage trend
    4. Frequency bounds: 49.5 Hz ≤ f ≤ 50.5 Hz (for 50Hz systems)
    5. Voltage bounds: 0.95 ≤ V ≤ 1.05 p.u.

Violations indicate cyber manipulation.

Output:
    - physics_violation_score ∈ [0,1]
    - confidence score
    - human-readable reason
"""

from typing import Dict, Any, List, Tuple
from ai_config import AIEngineConfig


class PhysicsValidationModel:
    """Validates telemetry against physical laws of power systems"""
    
    def __init__(self):
        self.config = AIEngineConfig.PHYSICS_CONFIG
        self.name = "Physics-Aware Validation"
        
    def analyze(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate telemetry against physics laws
        
        Args:
            preprocessed_data: Preprocessed telemetry data
            
        Returns:
            dict: {
                'score': float [0,1],
                'confidence': float [0,1],
                'reason': str,
                'details': dict
            }
        """
        violations = []
        violation_scores = []
        
        # Check 1: Breaker-Power Consistency
        score, reason = self._check_breaker_power_consistency(preprocessed_data)
        if score > 0:
            violations.append(reason)
            violation_scores.append(score)
        
        # Check 2: Voltage Bounds
        score, reason = self._check_voltage_bounds(preprocessed_data)
        if score > 0:
            violations.append(reason)
            violation_scores.append(score)
        
        # Check 3: Frequency Bounds
        score, reason = self._check_frequency_bounds(preprocessed_data)
        if score > 0:
            violations.append(reason)
            violation_scores.append(score)
        
        # Check 4: Power-Voltage Causality
        score, reason = self._check_power_voltage_causality(preprocessed_data)
        if score > 0:
            violations.append(reason)
            violation_scores.append(score)
        
        # Check 5: Physical Impossibilities
        score, reason = self._check_physical_impossibilities(preprocessed_data)
        if score > 0:
            violations.append(reason)
            violation_scores.append(score)
        
        # Aggregate results
        if not violations:
            return {
                'score': 0.0,
                'confidence': 0.98,
                'reason': 'All physics constraints satisfied',
                'details': {
                    'checks_performed': 5,
                    'violations_found': 0
                }
            }
        
        # Calculate final violation score (max of all violations)
        final_score = max(violation_scores)
        
        # High confidence in physics violations
        confidence = 0.95
        
        # Primary violation
        primary_reason = violations[0]
        if len(violations) > 1:
            primary_reason += f" (+{len(violations)-1} more violations)"
        
        return {
            'score': final_score,
            'confidence': confidence,
            'reason': primary_reason,
            'details': {
                'checks_performed': 5,
                'violations_found': len(violations),
                'all_violations': violations
            }
        }
    
    def _check_breaker_power_consistency(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check: breaker_status == "OFF" ⇒ power_flow ≈ 0
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        breaker_status = data.get('breaker_status', 'ON')
        power_flow = data.get('power_flow', 0.0)
        tolerance = self.config['breaker_off_power_tolerance']
        
        if breaker_status == 'OFF' and abs(power_flow) > tolerance:
            # CRITICAL VIOLATION: Power flowing through open breaker
            score = 1.0
            reason = f"CRITICAL: Power flow {power_flow:.2f} MW with breaker OFF"
            return score, reason
        
        return 0.0, ""
    
    def _check_voltage_bounds(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check: 0.95 ≤ V ≤ 1.05 p.u.
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        voltage = data.get('voltage', 1.0)
        v_min = self.config['voltage_min']
        v_max = self.config['voltage_max']
        
        if voltage < v_min:
            # Under-voltage violation
            deviation = (v_min - voltage) / v_min
            score = min(1.0, deviation * 5)  # Scale violation
            reason = f"Voltage {voltage:.3f} p.u. below physical minimum {v_min}"
            return score, reason
        
        if voltage > v_max:
            # Over-voltage violation
            deviation = (voltage - v_max) / v_max
            score = min(1.0, deviation * 5)
            reason = f"Voltage {voltage:.3f} p.u. exceeds physical maximum {v_max}"
            return score, reason
        
        return 0.0, ""
    
    def _check_frequency_bounds(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check: 49.5 Hz ≤ f ≤ 50.5 Hz (for 50Hz systems)
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        frequency = data.get('frequency', 50.0)
        f_min = self.config['frequency_min']
        f_max = self.config['frequency_max']
        
        if frequency < f_min:
            # Under-frequency violation
            deviation = (f_min - frequency) / f_min
            score = min(1.0, deviation * 10)
            reason = f"Frequency {frequency:.2f} Hz below physical minimum {f_min}"
            return score, reason
        
        if frequency > f_max:
            # Over-frequency violation
            deviation = (frequency - f_max) / f_max
            score = min(1.0, deviation * 10)
            reason = f"Frequency {frequency:.2f} Hz exceeds physical maximum {f_max}"
            return score, reason
        
        return 0.0, ""
    
    def _check_power_voltage_causality(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check: Power trend should follow voltage trend
        
        In power systems: P ∝ V² (roughly)
        If V increases, P should increase (and vice versa)
        
        Args:
            data: Telemetry data with deltas
            
        Returns:
            tuple: (score, reason)
        """
        delta_v = data.get('delta_voltage', 0)
        delta_p = data.get('delta_power_flow', 0)
        
        # Only check if both are changing significantly
        if abs(delta_v) > 0.02 and abs(delta_p) > 3.0:
            # Check if they're moving in opposite directions
            if (delta_v > 0 and delta_p < 0) or (delta_v < 0 and delta_p > 0):
                score = 0.6
                reason = "Power-voltage causality violation (opposite trends)"
                return score, reason
        
        return 0.0, ""
    
    def _check_physical_impossibilities(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check for physically impossible scenarios
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        voltage = data.get('voltage', 1.0)
        frequency = data.get('frequency', 50.0)
        power_flow = data.get('power_flow', 0.0)
        
        # Check 1: Zero voltage but non-zero frequency (impossible)
        if voltage < 0.01 and frequency > 1.0:
            score = 1.0
            reason = "CRITICAL: Frequency exists without voltage (impossible)"
            return score, reason
        
        # Check 2: Zero voltage but non-zero power (impossible)
        if voltage < 0.01 and abs(power_flow) > 1.0:
            score = 1.0
            reason = "CRITICAL: Power flow without voltage (impossible)"
            return score, reason
        
        # Check 3: Extreme rate of change (physically impossible)
        delta_f = abs(data.get('delta_frequency', 0))
        delta_time = data.get('delta_time', 1.0)
        
        if delta_time > 0:
            freq_rate = delta_f / delta_time  # Hz per second
            if freq_rate > 2.0:  # More than 2 Hz/sec is physically impossible
                score = 0.8
                reason = f"Physically impossible frequency rate of change: {freq_rate:.2f} Hz/s"
                return score, reason
        
        return 0.0, ""
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        return {
            'name': self.name,
            'type': 'physics_validation',
            'methods': [
                'breaker_power_consistency',
                'voltage_bounds',
                'frequency_bounds',
                'power_voltage_causality',
                'physical_impossibilities'
            ],
            'config': self.config
        }


# Utility function for quick physics check
def quick_physics_check(voltage: float, frequency: float, power_flow: float,
                       breaker_status: str) -> Tuple[bool, str]:
    """
    Quick physics validation check
    
    Args:
        voltage: Voltage in p.u.
        frequency: Frequency in Hz
        power_flow: Power flow in MW
        breaker_status: 'ON' or 'OFF'
        
    Returns:
        tuple: (is_valid, reason)
    """
    # Check breaker-power consistency
    if breaker_status == 'OFF' and abs(power_flow) > 0.01:
        return False, "Power flowing through open breaker"
    
    # Check voltage bounds
    if voltage < 0.95 or voltage > 1.05:
        return False, f"Voltage {voltage} out of bounds"
    
    # Check frequency bounds
    if frequency < 49.5 or frequency > 50.5:
        return False, f"Frequency {frequency} out of bounds"
    
    return True, "Valid"
