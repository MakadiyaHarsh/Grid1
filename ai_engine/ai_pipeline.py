"""
AI Pipeline - Main Orchestrator

This is the main entry point for the Multi-Model AI Engine.
It orchestrates the entire analysis pipeline:
    1. Preprocessing
    2. Parallel model execution
    3. Fusion
    4. Decision making
    5. Explainable output generation

Main Interface:
    analyze(input_data: dict) -> dict
"""

from typing import Dict, Any
from preprocessing import DataPreprocessor
from models.anomaly_model import AnomalyDetectionModel
from models.fdia_model import FDIADetectionModel
from models.physics_model import PhysicsValidationModel
from models.behavior_model import BehaviorLearningModel
from models.memory_model import MemoryModel
from fusion_engine import FusionEngine
from ai_config import AIEngineConfig


class AIPipeline:
    """Main AI Pipeline orchestrator for multi-model analysis"""
    
    def __init__(self):
        # Initialize preprocessor
        self.preprocessor = DataPreprocessor()
        
        # Initialize all AI models
        self.anomaly_model = AnomalyDetectionModel()
        self.fdia_model = FDIADetectionModel()
        self.physics_model = PhysicsValidationModel()
        self.behavior_model = BehaviorLearningModel()
        self.memory_model = MemoryModel()
        
        # Initialize fusion engine
        self.fusion_engine = FusionEngine()
        
        # Pipeline metadata
        self.analysis_count = 0
        
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main AI analysis function
        
        This is the primary interface for the cybersecurity gateway.
        
        Args:
            input_data: Raw telemetry data
                {
                    "voltage": float,           # Voltage in p.u.
                    "frequency": float,         # Frequency in Hz
                    "power_flow": float,        # Power flow in MW
                    "breaker_status": str,      # "ON" or "OFF"
                    "timestamp": str            # ISO format timestamp
                }
        
        Returns:
            dict: Complete AI analysis result
                {
                    "model_outputs": {
                        "anomaly": float,
                        "fdia": float,
                        "physics": float,
                        "behavior": float,
                        "memory": float
                    },
                    "final_risk": float,
                    "decision": str,
                    "confidence": float,
                    "explanation": str,
                    "details": dict
                }
        """
        try:
            # Step 1: Preprocess input data
            preprocessed_data = self.preprocessor.preprocess(input_data)
            
            # Step 2: Execute all models in parallel (conceptually)
            model_outputs = self._execute_models(preprocessed_data)
            
            # Step 3: Fuse model outputs
            fusion_result = self.fusion_engine.fuse(model_outputs)
            
            # Step 4: Prepare final output
            final_output = self._prepare_output(
                model_outputs, fusion_result, preprocessed_data
            )
            
            # Update analysis count
            self.analysis_count += 1
            
            return final_output
            
        except Exception as e:
            # Error handling
            return self._handle_error(e, input_data)
    
    def _execute_models(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Execute all AI models
        
        Args:
            preprocessed_data: Preprocessed telemetry
            
        Returns:
            dict: All model outputs
        """
        # Get telemetry history and rolling statistics
        telemetry_history = self.preprocessor.get_history()
        
        # Rolling statistics for anomaly detection
        rolling_stats = {}
        window = AIEngineConfig.ANOMALY_CONFIG['rolling_window']
        for field in ['voltage', 'frequency', 'power_flow']:
            rolling_stats[field] = self.preprocessor.get_rolling_statistics(field, window)
        
        # Execute each model
        model_outputs = {}
        
        # MODEL-1: Anomaly Detection
        model_outputs['anomaly'] = self.anomaly_model.analyze(
            preprocessed_data, rolling_stats
        )
        
        # MODEL-2: FDIA Detection
        model_outputs['fdia'] = self.fdia_model.analyze(
            preprocessed_data, telemetry_history
        )
        
        # MODEL-3: Physics Validation
        model_outputs['physics'] = self.physics_model.analyze(
            preprocessed_data
        )
        
        # MODEL-4: Behavior Learning
        model_outputs['behavior'] = self.behavior_model.analyze(
            preprocessed_data
        )
        
        # MODEL-5: Memory & Similarity
        model_outputs['memory'] = self.memory_model.analyze(
            preprocessed_data, telemetry_history
        )
        
        return model_outputs
    
    def _prepare_output(self, model_outputs: Dict[str, Dict[str, Any]],
                       fusion_result: Dict[str, Any],
                       preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare final output in required format
        
        Args:
            model_outputs: All model outputs
            fusion_result: Fusion engine result
            preprocessed_data: Preprocessed data
            
        Returns:
            dict: Final formatted output
        """
        # Extract model scores
        model_scores = {
            key: output.get('score', 0.0)
            for key, output in model_outputs.items()
        }
        
        return {
            # Required output format
            "model_outputs": model_scores,
            "final_risk": fusion_result['final_risk'],
            "decision": fusion_result['decision'],
            "confidence": fusion_result['confidence'],
            "explanation": fusion_result['explanation'],
            
            # Additional details
            "details": {
                "primary_threat": fusion_result['primary_threat'],
                "primary_threat_score": fusion_result['primary_threat_score'],
                "model_contributions": fusion_result['model_contributions'],
                "individual_reasons": {
                    key: output.get('reason', '')
                    for key, output in model_outputs.items()
                },
                "analysis_count": self.analysis_count,
                "input_data": {
                    "voltage": preprocessed_data.get('voltage'),
                    "frequency": preprocessed_data.get('frequency'),
                    "power_flow": preprocessed_data.get('power_flow'),
                    "breaker_status": preprocessed_data.get('breaker_status')
                }
            }
        }
    
    def _handle_error(self, error: Exception, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle analysis errors gracefully
        
        Args:
            error: Exception that occurred
            input_data: Original input data
            
        Returns:
            dict: Error response
        """
        return {
            "model_outputs": {
                "anomaly": 0.0,
                "fdia": 0.0,
                "physics": 0.0,
                "behavior": 0.0,
                "memory": 0.0
            },
            "final_risk": 0.0,
            "decision": "ERROR",
            "confidence": 0.0,
            "explanation": f"Analysis error: {str(error)}",
            "details": {
                "error": str(error),
                "error_type": type(error).__name__,
                "input_data": input_data
            }
        }
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """
        Get pipeline statistics
        
        Returns:
            dict: Pipeline statistics
        """
        return {
            "analysis_count": self.analysis_count,
            "preprocessor_history_size": len(self.preprocessor.telemetry_history),
            "memory_stats": self.memory_model.get_memory_stats(),
            "behavior_profile": self.behavior_model.get_behavior_profile(),
            "fusion_weights": self.fusion_engine.get_weights()
        }
    
    def reset(self) -> None:
        """Reset pipeline state (useful for testing)"""
        self.preprocessor.reset()
        self.fdia_model.history = []
        self.behavior_model.command_history = []
        self.behavior_model.timestamp_history = []
        self.memory_model.telemetry_memory = []
        self.analysis_count = 0


# Global pipeline instance (singleton pattern)
_pipeline_instance = None


def get_pipeline() -> AIPipeline:
    """
    Get global pipeline instance (singleton)
    
    Returns:
        AIPipeline: Global pipeline instance
    """
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = AIPipeline()
    return _pipeline_instance


def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main analysis function (convenience wrapper)
    
    This is the primary interface for external integration.
    
    Args:
        input_data: Raw telemetry data
        
    Returns:
        dict: Analysis result
        
    Example:
        >>> result = analyze({
        ...     "voltage": 1.02,
        ...     "frequency": 50.1,
        ...     "power_flow": 105.3,
        ...     "breaker_status": "ON",
        ...     "timestamp": "2026-01-31T03:00:00"
        ... })
        >>> print(result['decision'])
        'SAFE'
    """
    pipeline = get_pipeline()
    return pipeline.analyze(input_data)


# Expose main interface
__all__ = ['analyze', 'AIPipeline', 'get_pipeline']
