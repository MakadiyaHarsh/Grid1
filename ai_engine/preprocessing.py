"""
Preprocessing Module for Multi-Model AI Engine

This module handles:
- Input validation and schema checking
- Data normalization to [0,1] range
- Missing field handling with defaults
- Temporal feature extraction (deltas, time-based features)
- Feature engineering for AI models
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import math
from ai_config import AIEngineConfig


class PreprocessingError(Exception):
    """Custom exception for preprocessing errors"""
    pass


class DataPreprocessor:
    """Preprocesses telemetry data for AI model consumption"""
    
    def __init__(self):
        self.config = AIEngineConfig.PREPROCESSING_CONFIG
        self.last_telemetry: Optional[Dict[str, Any]] = None
        self.telemetry_history = []
        
    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main preprocessing pipeline
        
        Args:
            input_data: Raw telemetry data
            
        Returns:
            dict: Preprocessed and enriched data
            
        Raises:
            PreprocessingError: If input validation fails
        """
        # Step 1: Validate input schema
        validated_data = self._validate_input(input_data)
        
        # Step 2: Handle missing fields
        complete_data = self._handle_missing_fields(validated_data)
        
        # Step 3: Normalize numerical values
        normalized_data = self._normalize_values(complete_data)
        
        # Step 4: Extract temporal features
        temporal_features = self._extract_temporal_features(complete_data)
        
        # Step 5: Compute deltas (changes from previous reading)
        delta_features = self._compute_deltas(complete_data)
        
        # Step 6: Combine all features
        preprocessed_data = {
            **complete_data,           # Original data
            **normalized_data,         # Normalized values
            **temporal_features,       # Time-based features
            **delta_features          # Delta features
        }
        
        # Update history
        self._update_history(complete_data)
        
        return preprocessed_data
    
    def _validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input data schema
        
        Args:
            input_data: Raw input data
            
        Returns:
            dict: Validated data
            
        Raises:
            PreprocessingError: If validation fails
        """
        if not isinstance(input_data, dict):
            raise PreprocessingError("Input must be a dictionary")
        
        # Required fields (at least one telemetry value must be present)
        telemetry_fields = ['voltage', 'frequency', 'power_flow']
        has_telemetry = any(field in input_data for field in telemetry_fields)
        
        if not has_telemetry:
            raise PreprocessingError(
                f"At least one telemetry field required: {telemetry_fields}"
            )
        
        # Validate data types
        if 'voltage' in input_data and not isinstance(input_data['voltage'], (int, float)):
            raise PreprocessingError("Voltage must be numeric")
        
        if 'frequency' in input_data and not isinstance(input_data['frequency'], (int, float)):
            raise PreprocessingError("Frequency must be numeric")
        
        if 'power_flow' in input_data and not isinstance(input_data['power_flow'], (int, float)):
            raise PreprocessingError("Power flow must be numeric")
        
        if 'breaker_status' in input_data and input_data['breaker_status'] not in ['ON', 'OFF']:
            raise PreprocessingError("Breaker status must be 'ON' or 'OFF'")
        
        return input_data
    
    def _handle_missing_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill missing fields with default values
        
        Args:
            data: Validated input data
            
        Returns:
            dict: Complete data with defaults
        """
        complete_data = data.copy()
        defaults = self.config['default_values']
        
        for field, default_value in defaults.items():
            if field not in complete_data:
                complete_data[field] = default_value
        
        # Handle timestamp
        if 'timestamp' not in complete_data:
            complete_data['timestamp'] = datetime.now().isoformat()
        
        return complete_data
    
    def _normalize_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize numerical values to [0, 1] range
        
        Args:
            data: Complete data
            
        Returns:
            dict: Normalized values with '_norm' suffix
        """
        normalized = {}
        ranges = self.config['normalization_ranges']
        
        for field, (min_val, max_val) in ranges.items():
            if field in data:
                value = data[field]
                # Clamp to range
                value = max(min_val, min(max_val, value))
                # Normalize to [0, 1]
                normalized[f'{field}_norm'] = (value - min_val) / (max_val - min_val)
        
        return normalized
    
    def _extract_temporal_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract time-based features from timestamp
        
        Args:
            data: Complete data with timestamp
            
        Returns:
            dict: Temporal features
        """
        try:
            timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            # Fallback to current time if parsing fails
            timestamp = datetime.now()
        
        return {
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'is_weekend': timestamp.weekday() >= 5,
            'is_night': timestamp.hour < 6 or timestamp.hour >= 22,
            'timestamp_unix': timestamp.timestamp()
        }
    
    def _compute_deltas(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute changes from previous telemetry reading
        
        Args:
            data: Current telemetry data
            
        Returns:
            dict: Delta features with 'delta_' prefix
        """
        deltas = {}
        
        if self.last_telemetry is None:
            # First reading - no deltas
            deltas['delta_voltage'] = 0.0
            deltas['delta_frequency'] = 0.0
            deltas['delta_power_flow'] = 0.0
            deltas['delta_time'] = 0.0
        else:
            # Compute deltas
            deltas['delta_voltage'] = data['voltage'] - self.last_telemetry['voltage']
            deltas['delta_frequency'] = data['frequency'] - self.last_telemetry['frequency']
            deltas['delta_power_flow'] = data['power_flow'] - self.last_telemetry['power_flow']
            
            # Time delta
            try:
                current_time = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                last_time = datetime.fromisoformat(self.last_telemetry['timestamp'].replace('Z', '+00:00'))
                deltas['delta_time'] = (current_time - last_time).total_seconds()
            except (ValueError, AttributeError):
                deltas['delta_time'] = 0.0
            
            # Breaker state change
            deltas['breaker_changed'] = (
                data['breaker_status'] != self.last_telemetry['breaker_status']
            )
        
        # Store current as last for next iteration
        self.last_telemetry = data.copy()
        
        return deltas
    
    def _update_history(self, data: Dict[str, Any]) -> None:
        """
        Update telemetry history for statistical analysis
        
        Args:
            data: Current telemetry data
        """
        self.telemetry_history.append({
            'voltage': data['voltage'],
            'frequency': data['frequency'],
            'power_flow': data['power_flow'],
            'timestamp': data['timestamp']
        })
        
        # Keep only last N samples (configured in memory config)
        max_history = AIEngineConfig.MEMORY_CONFIG['history_size']
        if len(self.telemetry_history) > max_history:
            self.telemetry_history.pop(0)
    
    def get_rolling_statistics(self, field: str, window: int) -> Tuple[float, float]:
        """
        Compute rolling mean and standard deviation
        
        Args:
            field: Field name ('voltage', 'frequency', 'power_flow')
            window: Rolling window size
            
        Returns:
            tuple: (mean, std_dev)
        """
        if len(self.telemetry_history) < 2:
            return 0.0, 0.0
        
        # Get last N samples
        samples = [h[field] for h in self.telemetry_history[-window:]]
        
        # Compute mean
        mean = sum(samples) / len(samples)
        
        # Compute standard deviation
        variance = sum((x - mean) ** 2 for x in samples) / len(samples)
        std_dev = math.sqrt(variance)
        
        return mean, std_dev
    
    def get_history(self, limit: Optional[int] = None) -> list:
        """
        Get telemetry history
        
        Args:
            limit: Maximum number of samples to return
            
        Returns:
            list: Historical telemetry data
        """
        if limit is None:
            return self.telemetry_history.copy()
        return self.telemetry_history[-limit:]
    
    def reset(self) -> None:
        """Reset preprocessor state"""
        self.last_telemetry = None
        self.telemetry_history = []


# Utility functions for external use

def validate_telemetry(data: Dict[str, Any]) -> bool:
    """
    Quick validation check for telemetry data
    
    Args:
        data: Telemetry data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        preprocessor = DataPreprocessor()
        preprocessor._validate_input(data)
        return True
    except PreprocessingError:
        return False


def normalize_value(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize a single value to [0, 1] range
    
    Args:
        value: Value to normalize
        min_val: Minimum expected value
        max_val: Maximum expected value
        
    Returns:
        float: Normalized value
    """
    value = max(min_val, min(max_val, value))
    return (value - min_val) / (max_val - min_val)
