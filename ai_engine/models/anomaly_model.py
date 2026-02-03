"""
Statistical Anomaly Detection Model (MODEL-1)

Purpose:
    Detect deviation from normal grid behavior using statistical methods

Input:
    - voltage, frequency, power_flow, timestamp
    - preprocessed data with rolling statistics

Methods:
    - Rolling mean and standard deviation
    - Z-score calculation
    - Deviation percentage

Output:
    - anomaly_score ∈ [0,1]
    - confidence score
    - human-readable reason
"""

from typing import Dict, Any, Tuple
import math
from ai_config import AIEngineConfig


class AnomalyDetectionModel:
    """Statistical anomaly detection using z-score and deviation analysis"""
    
    def __init__(self):
        self.config = AIEngineConfig.ANOMALY_CONFIG
        self.name = "Statistical Anomaly Detection"
        
    def analyze(self, preprocessed_data: Dict[str, Any], 
                rolling_stats: Dict[str, Tuple[float, float]]) -> Dict[str, Any]:
        """
        Detect statistical anomalies in telemetry data
        
        Args:
            preprocessed_data: Preprocessed telemetry data
            rolling_stats: Dictionary of (mean, std_dev) for each field
            
        Returns:
            dict: {
                'score': float [0,1],
                'confidence': float [0,1],
                'reason': str,
                'details': dict
            }
        """
        anomaly_scores = []
        anomaly_details = []
        
        # Check each telemetry field
        fields = ['voltage', 'frequency', 'power_flow']
        
        for field in fields:
            if field in preprocessed_data and field in rolling_stats:
                value = preprocessed_data[field]
                mean, std_dev = rolling_stats[field]
                
                # Compute z-score
                z_score = self._compute_z_score(value, mean, std_dev)
                
                # Compute deviation percentage
                deviation_pct = self._compute_deviation_percentage(value, mean)
                
                # Determine if anomalous
                is_anomalous, score, reason = self._evaluate_anomaly(
                    field, value, z_score, deviation_pct, mean, std_dev
                )
                
                if is_anomalous:
                    anomaly_scores.append(score)
                    anomaly_details.append(reason)
        
        # Aggregate results
        if not anomaly_scores:
            # No anomalies detected
            return {
                'score': 0.0,
                'confidence': 0.95,
                'reason': 'All parameters within normal statistical range',
                'details': {
                    'anomalies_detected': 0,
                    'fields_checked': len(fields)
                }
            }
        
        # Calculate overall anomaly score (max of individual scores)
        final_score = max(anomaly_scores)
        
        # Confidence based on number of anomalies
        confidence = min(0.95, 0.6 + (len(anomaly_scores) * 0.15))
        
        # Combine reasons
        primary_reason = anomaly_details[0]
        if len(anomaly_details) > 1:
            primary_reason += f" ({len(anomaly_details)} anomalies total)"
        
        return {
            'score': final_score,
            'confidence': confidence,
            'reason': primary_reason,
            'details': {
                'anomalies_detected': len(anomaly_scores),
                'all_reasons': anomaly_details,
                'fields_checked': len(fields)
            }
        }
    
    def _compute_z_score(self, value: float, mean: float, std_dev: float) -> float:
        """
        Compute z-score: z = (x - μ) / σ
        
        Args:
            value: Current value
            mean: Rolling mean
            std_dev: Rolling standard deviation
            
        Returns:
            float: Z-score
        """
        if std_dev == 0:
            return 0.0
        return abs(value - mean) / std_dev
    
    def _compute_deviation_percentage(self, value: float, mean: float) -> float:
        """
        Compute deviation percentage: |x - μ| / μ × 100%
        
        Args:
            value: Current value
            mean: Rolling mean
            
        Returns:
            float: Deviation percentage
        """
        if mean == 0:
            return 0.0
        return abs(value - mean) / abs(mean)
    
    def _evaluate_anomaly(self, field: str, value: float, z_score: float, 
                         deviation_pct: float, mean: float, 
                         std_dev: float) -> Tuple[bool, float, str]:
        """
        Evaluate if value is anomalous
        
        Args:
            field: Field name
            value: Current value
            z_score: Computed z-score
            deviation_pct: Deviation percentage
            mean: Rolling mean
            std_dev: Standard deviation
            
        Returns:
            tuple: (is_anomalous, score, reason)
        """
        z_threshold = self.config['z_score_threshold']
        dev_threshold = self.config['deviation_threshold']
        
        # Check z-score threshold
        if z_score > z_threshold:
            # High z-score indicates anomaly
            score = min(1.0, z_score / (z_threshold * 2))
            reason = f"{field.capitalize()} deviation {z_score:.1f}σ from rolling mean"
            return True, score, reason
        
        # Check deviation percentage threshold
        if deviation_pct > dev_threshold:
            # High deviation percentage
            score = min(1.0, deviation_pct / (dev_threshold * 2))
            reason = f"{field.capitalize()} deviated {deviation_pct*100:.1f}% from expected"
            return True, score, reason
        
        # No anomaly detected
        return False, 0.0, ""
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        return {
            'name': self.name,
            'type': 'statistical',
            'methods': ['z-score', 'deviation_percentage', 'rolling_statistics'],
            'config': self.config
        }


# Standalone function for quick anomaly check
def quick_anomaly_check(value: float, mean: float, std_dev: float, 
                       threshold: float = 2.5) -> bool:
    """
    Quick anomaly check using z-score
    
    Args:
        value: Current value
        mean: Expected mean
        std_dev: Expected standard deviation
        threshold: Z-score threshold
        
    Returns:
        bool: True if anomalous
    """
    if std_dev == 0:
        return False
    z_score = abs(value - mean) / std_dev
    return z_score > threshold
