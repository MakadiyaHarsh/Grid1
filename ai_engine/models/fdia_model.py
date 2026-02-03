"""
False Data Injection Attack Detection Model (MODEL-2)

Purpose:
    Detect coordinated multi-parameter manipulation even when residual is constant
    
Mathematical Basis:
    Traditional SCADA: z = H·x + e
    FDIA Attack: z' = z + H·c  →  r' = r (residual unchanged!)
    
    Our approach detects FDIA through:
    - Correlation mismatch (V-f correlation breaks)
    - Temporal consistency check
    - Multi-signal coordination analysis

Output:
    - fdia_score ∈ [0,1]
    - confidence score
    - human-readable reason
"""

from typing import Dict, Any, List, Tuple
import math
from ai_config import AIEngineConfig


class FDIADetectionModel:
    """Detects False Data Injection Attacks using correlation and coordination analysis"""
    
    def __init__(self):
        self.config = AIEngineConfig.FDIA_CONFIG
        self.name = "FDIA Detection"
        self.history: List[Dict[str, float]] = []
        
    def analyze(self, preprocessed_data: Dict[str, Any], 
                telemetry_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect False Data Injection Attacks
        
        Args:
            preprocessed_data: Current preprocessed telemetry
            telemetry_history: Historical telemetry data
            
        Returns:
            dict: {
                'score': float [0,1],
                'confidence': float [0,1],
                'reason': str,
                'details': dict
            }
        """
        # Update internal history
        self._update_history(preprocessed_data)
        
        fdia_indicators = []
        fdia_scores = []
        
        # Check 1: Voltage-Frequency Correlation Mismatch
        corr_score, corr_reason = self._check_correlation_mismatch(
            preprocessed_data, telemetry_history
        )
        if corr_score > 0:
            fdia_scores.append(corr_score)
            fdia_indicators.append(corr_reason)
        
        # Check 2: Temporal Consistency
        temp_score, temp_reason = self._check_temporal_consistency(
            preprocessed_data
        )
        if temp_score > 0:
            fdia_scores.append(temp_score)
            fdia_indicators.append(temp_reason)
        
        # Check 3: Multi-Signal Coordination
        coord_score, coord_reason = self._check_multi_signal_coordination(
            preprocessed_data
        )
        if coord_score > 0:
            fdia_scores.append(coord_score)
            fdia_indicators.append(coord_reason)
        
        # Aggregate results
        if not fdia_scores:
            return {
                'score': 0.0,
                'confidence': 0.85,
                'reason': 'No FDIA indicators detected',
                'details': {
                    'checks_performed': 3,
                    'indicators_found': 0
                }
            }
        
        # Calculate final FDIA score (average of indicators)
        final_score = sum(fdia_scores) / len(fdia_scores)
        
        # Confidence increases with number of indicators
        confidence = min(0.95, 0.7 + (len(fdia_indicators) * 0.1))
        
        # Primary reason
        primary_reason = "Coordinated false data injection detected"
        if len(fdia_indicators) == 1:
            primary_reason = fdia_indicators[0]
        
        return {
            'score': final_score,
            'confidence': confidence,
            'reason': primary_reason,
            'details': {
                'checks_performed': 3,
                'indicators_found': len(fdia_indicators),
                'all_indicators': fdia_indicators
            }
        }
    
    def _check_correlation_mismatch(self, current_data: Dict[str, Any],
                                   history: List[Dict[str, Any]]) -> Tuple[float, str]:
        """
        Check for voltage-frequency correlation mismatch
        
        In normal operation: corr(V, f) ≈ 0.8-0.9
        During FDIA: corr(V, f) < 0.3 (coordinated injection breaks correlation)
        
        Args:
            current_data: Current telemetry
            history: Historical data
            
        Returns:
            tuple: (score, reason)
        """
        if len(history) < 5:
            return 0.0, ""
        
        # Get recent voltage and frequency values
        recent_window = history[-self.config['temporal_window']:]
        voltages = [h['voltage'] for h in recent_window]
        frequencies = [h['frequency'] for h in recent_window]
        
        # Compute correlation
        correlation = self._compute_correlation(voltages, frequencies)
        
        # Check if correlation is broken
        expected_corr = self.config['normal_correlation']
        threshold = self.config['correlation_threshold']
        
        if correlation < threshold:
            # Correlation mismatch detected
            score = 1.0 - (correlation / threshold)  # Lower correlation = higher score
            reason = f"V-f correlation breakdown ({correlation:.2f} vs expected {expected_corr:.2f})"
            return score, reason
        
        return 0.0, ""
    
    def _check_temporal_consistency(self, current_data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check for sudden coordinated changes across parameters
        
        FDIA often causes simultaneous jumps in multiple parameters
        
        Args:
            current_data: Current telemetry with deltas
            
        Returns:
            tuple: (score, reason)
        """
        # Check if multiple parameters changed significantly at once
        delta_voltage = abs(current_data.get('delta_voltage', 0))
        delta_frequency = abs(current_data.get('delta_frequency', 0))
        delta_power = abs(current_data.get('delta_power_flow', 0))
        
        # Thresholds for "significant" change
        v_threshold = 0.05  # 5% voltage change
        f_threshold = 0.2   # 0.2 Hz frequency change
        p_threshold = 10.0  # 10 MW power change
        
        significant_changes = 0
        if delta_voltage > v_threshold:
            significant_changes += 1
        if delta_frequency > f_threshold:
            significant_changes += 1
        if delta_power > p_threshold:
            significant_changes += 1
        
        # If 2 or more parameters changed significantly
        if significant_changes >= 2:
            score = min(1.0, significant_changes / 3.0 + 0.3)
            reason = f"Coordinated parameter changes detected ({significant_changes} simultaneous)"
            return score, reason
        
        return 0.0, ""
    
    def _check_multi_signal_coordination(self, current_data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check if power follows voltage but with suspicious coordination
        
        Normal: Power changes follow voltage changes naturally
        FDIA: Power and voltage change together but unnaturally coordinated
        
        Args:
            current_data: Current telemetry
            
        Returns:
            tuple: (score, reason)
        """
        if len(self.history) < 3:
            return 0.0, ""
        
        # Check if voltage and power are changing in same direction
        delta_v = current_data.get('delta_voltage', 0)
        delta_p = current_data.get('delta_power_flow', 0)
        
        # If both are changing significantly
        if abs(delta_v) > 0.03 and abs(delta_p) > 5.0:
            # Check if they're changing in opposite directions (suspicious)
            if (delta_v > 0 and delta_p < 0) or (delta_v < 0 and delta_p > 0):
                score = 0.7
                reason = "Power-voltage coordination anomaly (opposite directions)"
                return score, reason
            
            # Check if magnitude ratio is suspicious
            # Normal P-V relationship: ΔP ≈ 2·ΔV (rough approximation)
            expected_ratio = 2.0
            actual_ratio = abs(delta_p / delta_v) if delta_v != 0 else 0
            
            if actual_ratio > expected_ratio * 3 or actual_ratio < expected_ratio / 3:
                score = 0.6
                reason = "Suspicious power-voltage magnitude coordination"
                return score, reason
        
        return 0.0, ""
    
    def _compute_correlation(self, x: List[float], y: List[float]) -> float:
        """
        Compute Pearson correlation coefficient
        
        Args:
            x: First variable
            y: Second variable
            
        Returns:
            float: Correlation coefficient [-1, 1]
        """
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        
        sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        
        if denominator == 0:
            return 0.0
        
        return abs(numerator / denominator)  # Return absolute correlation
    
    def _update_history(self, data: Dict[str, Any]) -> None:
        """Update internal history for correlation analysis"""
        self.history.append({
            'voltage': data['voltage'],
            'frequency': data['frequency'],
            'power_flow': data['power_flow']
        })
        
        # Keep only recent history
        max_history = 50
        if len(self.history) > max_history:
            self.history.pop(0)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        return {
            'name': self.name,
            'type': 'correlation_analysis',
            'methods': ['correlation_mismatch', 'temporal_consistency', 'multi_signal_coordination'],
            'config': self.config
        }
