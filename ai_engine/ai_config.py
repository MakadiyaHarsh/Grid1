"""
Configuration System for Multi-Model AI Engine

This module contains all configurable parameters for the AI engine including:
- Model fusion weights
- Decision thresholds
- Anomaly detection parameters
- Physics validation rules
- Behavioral learning parameters
- Memory system configuration
"""

from typing import Dict, Any


class AIEngineConfig:
    """Central configuration for the Multi-Model AI Engine"""
    
    # ========== FUSION ENGINE WEIGHTS ==========
    # These weights determine how much each model contributes to final risk score
    # Sum should equal 1.0 for normalized output
    FUSION_WEIGHTS = {
        'anomaly': 0.15,      # Statistical anomaly detection
        'fdia': 0.35,         # False Data Injection Attack (highest priority)
        'physics': 0.25,      # Physics-aware validation
        'behavior': 0.10,     # Behavioral pattern learning
        'memory': 0.15        # Historical memory & similarity
    }
    
    # ========== DECISION THRESHOLDS ==========
    DECISION_THRESHOLDS = {
        'safe': 0.30,         # Risk < 0.30 → SAFE
        'warning': 0.60       # 0.30 ≤ Risk < 0.60 → WARNING, Risk ≥ 0.60 → CRITICAL
    }
    
    # ========== ANOMALY DETECTION PARAMETERS ==========
    ANOMALY_CONFIG = {
        'rolling_window': 20,           # Number of samples for rolling statistics
        'z_score_threshold': 2.5,       # Z-score threshold for anomaly detection
        'deviation_threshold': 0.15,    # 15% deviation threshold
        'min_samples': 5                # Minimum samples before anomaly detection
    }
    
    # ========== FDIA DETECTION PARAMETERS ==========
    FDIA_CONFIG = {
        'correlation_threshold': 0.3,   # Minimum expected V-f correlation
        'normal_correlation': 0.85,     # Normal V-f correlation baseline
        'temporal_window': 5,           # Samples to check temporal consistency
        'coordination_threshold': 0.7   # Multi-signal coordination threshold
    }
    
    # ========== PHYSICS VALIDATION RULES ==========
    PHYSICS_CONFIG = {
        # Voltage bounds (per unit)
        'voltage_min': 0.95,
        'voltage_max': 1.05,
        
        # Frequency bounds (Hz) - for 50Hz systems
        'frequency_min': 49.5,
        'frequency_max': 50.5,
        
        # Power flow tolerance when breaker is OFF
        'breaker_off_power_tolerance': 0.01,  # Allow 1% tolerance for measurement noise
        
        # Causality check window (seconds)
        'causality_window': 2.0,
        
        # Power-voltage correlation threshold
        'power_voltage_correlation': 0.6
    }
    
    # ========== BEHAVIORAL LEARNING PARAMETERS ==========
    BEHAVIOR_CONFIG = {
        'normal_hours': (6, 22),        # Normal operation hours (6 AM - 10 PM)
        'max_switches_per_hour': 10,    # Maximum acceptable breaker switches
        'command_interval_min': 5,      # Minimum seconds between commands
        'pattern_memory_size': 50,      # Number of command patterns to remember
        'replay_time_tolerance': 0.1    # Tolerance for timestamp replay detection (seconds)
    }
    
    # ========== MEMORY SYSTEM CONFIGURATION ==========
    MEMORY_CONFIG = {
        'history_size': 100,            # Number of telemetry points to store
        'attack_signature_db': [],      # Known attack signatures (populated at runtime)
        'similarity_threshold': 0.85,   # Cosine similarity threshold for attack matching
        'feature_weights': {            # Weights for similarity computation
            'voltage': 0.3,
            'frequency': 0.3,
            'power_flow': 0.4
        }
    }
    
    # ========== PREPROCESSING PARAMETERS ==========
    PREPROCESSING_CONFIG = {
        'normalization_ranges': {
            'voltage': (0.8, 1.2),      # Expected voltage range (p.u.)
            'frequency': (49.0, 51.0),  # Expected frequency range (Hz)
            'power_flow': (0, 200)      # Expected power range (MW)
        },
        'default_values': {
            'voltage': 1.0,
            'frequency': 50.0,
            'power_flow': 0.0,
            'breaker_status': 'OFF'
        }
    }
    
    # ========== EXPLAINABILITY TEMPLATES ==========
    EXPLANATION_TEMPLATES = {
        'safe': "All systems normal. {details}",
        'warning': "WARNING: {primary_reason}. {supporting_evidence}",
        'critical': "CRITICAL: {primary_reason}. {supporting_evidence}"
    }
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate configuration consistency
        
        Returns:
            bool: True if configuration is valid
        """
        # Check fusion weights sum to 1.0
        weight_sum = sum(cls.FUSION_WEIGHTS.values())
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(f"Fusion weights must sum to 1.0, got {weight_sum}")
        
        # Check decision thresholds are ordered
        if cls.DECISION_THRESHOLDS['safe'] >= cls.DECISION_THRESHOLDS['warning']:
            raise ValueError("Decision thresholds must be ordered: safe < warning")
        
        # Check all weights are positive
        for key, value in cls.FUSION_WEIGHTS.items():
            if value < 0:
                raise ValueError(f"Fusion weight '{key}' must be positive, got {value}")
        
        return True
    
    @classmethod
    def get_decision(cls, risk_score: float) -> str:
        """
        Get decision category based on risk score
        
        Args:
            risk_score: Risk score between 0 and 1
            
        Returns:
            str: Decision category ('SAFE', 'WARNING', or 'CRITICAL')
        """
        if risk_score < cls.DECISION_THRESHOLDS['safe']:
            return 'SAFE'
        elif risk_score < cls.DECISION_THRESHOLDS['warning']:
            return 'WARNING'
        else:
            return 'CRITICAL'
    
    @classmethod
    def update_weights(cls, new_weights: Dict[str, float]) -> None:
        """
        Update fusion weights dynamically
        
        Args:
            new_weights: Dictionary of new weights
        """
        # Validate new weights
        weight_sum = sum(new_weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(f"New weights must sum to 1.0, got {weight_sum}")
        
        cls.FUSION_WEIGHTS.update(new_weights)
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """
        Get a summary of current configuration
        
        Returns:
            dict: Configuration summary
        """
        return {
            'fusion_weights': cls.FUSION_WEIGHTS,
            'decision_thresholds': cls.DECISION_THRESHOLDS,
            'anomaly_config': cls.ANOMALY_CONFIG,
            'fdia_config': cls.FDIA_CONFIG,
            'physics_config': cls.PHYSICS_CONFIG,
            'behavior_config': cls.BEHAVIOR_CONFIG,
            'memory_config': cls.MEMORY_CONFIG
        }


# Validate configuration on module load
AIEngineConfig.validate_config()
