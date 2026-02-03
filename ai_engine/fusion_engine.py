"""
AI Fusion Engine

Purpose:
    Combine outputs from all AI models using weighted fusion
    
Mathematical Formula:
    Risk = w₁·A + w₂·F + w₃·P + w₄·B + w₅·M
    
Where:
    A = anomaly_score
    F = fdia_score
    P = physics_violation_score
    B = behavior_score
    M = memory_score
    
Weights are configurable in config.py
Default weights:
    w₁ = 0.15 (Anomaly)
    w₂ = 0.35 (FDIA - highest priority)
    w₃ = 0.25 (Physics)
    w₄ = 0.10 (Behavior)
    w₅ = 0.15 (Memory)
"""

from typing import Dict, Any, List
from ai_config import AIEngineConfig


class FusionEngine:
    """Combines outputs from multiple AI models into unified risk score"""
    
    def __init__(self):
        self.config = AIEngineConfig
        self.weights = self.config.FUSION_WEIGHTS.copy()
        
    def fuse(self, model_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fuse multiple model outputs into single risk assessment
        
        Args:
            model_outputs: Dictionary of model outputs
                {
                    'anomaly': {'score': 0.18, 'confidence': 0.85, 'reason': '...'},
                    'fdia': {'score': 0.72, 'confidence': 0.92, 'reason': '...'},
                    'physics': {'score': 0.12, 'confidence': 0.98, 'reason': '...'},
                    'behavior': {'score': 0.08, 'confidence': 0.75, 'reason': '...'},
                    'memory': {'score': 0.61, 'confidence': 0.88, 'reason': '...'}
                }
        
        Returns:
            dict: Fused output
                {
                    'final_risk': float [0,1],
                    'confidence': float [0,1],
                    'decision': str ('SAFE', 'WARNING', 'CRITICAL'),
                    'explanation': str,
                    'model_contributions': dict,
                    'primary_threat': str
                }
        """
        # Extract scores
        scores = {
            'anomaly': model_outputs.get('anomaly', {}).get('score', 0.0),
            'fdia': model_outputs.get('fdia', {}).get('score', 0.0),
            'physics': model_outputs.get('physics', {}).get('score', 0.0),
            'behavior': model_outputs.get('behavior', {}).get('score', 0.0),
            'memory': model_outputs.get('memory', {}).get('score', 0.0)
        }
        
        # Calculate weighted risk score
        final_risk = self._calculate_weighted_risk(scores)
        
        # Calculate overall confidence
        confidences = {
            key: model_outputs.get(key, {}).get('confidence', 0.5)
            for key in scores.keys()
        }
        overall_confidence = self._calculate_weighted_confidence(confidences)
        
        # Get decision based on risk score
        decision = self.config.get_decision(final_risk)
        
        # Identify primary threat
        primary_threat, primary_score = self._identify_primary_threat(scores)
        
        # Generate explanation
        explanation = self._generate_explanation(
            decision, primary_threat, model_outputs, scores
        )
        
        # Calculate model contributions
        contributions = self._calculate_contributions(scores)
        
        return {
            'final_risk': round(final_risk, 3),
            'confidence': round(overall_confidence, 3),
            'decision': decision,
            'explanation': explanation,
            'model_contributions': contributions,
            'primary_threat': primary_threat,
            'primary_threat_score': round(primary_score, 3)
        }
    
    def _calculate_weighted_risk(self, scores: Dict[str, float]) -> float:
        """
        Calculate weighted risk score
        
        Args:
            scores: Dictionary of model scores
            
        Returns:
            float: Weighted risk score [0,1]
        """
        risk = 0.0
        for model_name, score in scores.items():
            weight = self.weights.get(model_name, 0.0)
            risk += weight * score
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, risk))
    
    def _calculate_weighted_confidence(self, confidences: Dict[str, float]) -> float:
        """
        Calculate weighted overall confidence
        
        Args:
            confidences: Dictionary of model confidences
            
        Returns:
            float: Overall confidence [0,1]
        """
        weighted_confidence = 0.0
        for model_name, confidence in confidences.items():
            weight = self.weights.get(model_name, 0.0)
            weighted_confidence += weight * confidence
        
        return max(0.0, min(1.0, weighted_confidence))
    
    def _identify_primary_threat(self, scores: Dict[str, float]) -> tuple:
        """
        Identify the primary threat (highest scoring model)
        
        Args:
            scores: Dictionary of model scores
            
        Returns:
            tuple: (primary_threat_name, score)
        """
        if not scores:
            return 'none', 0.0
        
        primary = max(scores.items(), key=lambda x: x[1])
        return primary[0], primary[1]
    
    def _calculate_contributions(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate each model's contribution to final risk
        
        Args:
            scores: Dictionary of model scores
            
        Returns:
            dict: Model contributions
        """
        contributions = {}
        for model_name, score in scores.items():
            weight = self.weights.get(model_name, 0.0)
            contribution = weight * score
            contributions[model_name] = round(contribution, 3)
        
        return contributions
    
    def _generate_explanation(self, decision: str, primary_threat: str,
                            model_outputs: Dict[str, Dict[str, Any]],
                            scores: Dict[str, float]) -> str:
        """
        Generate human-readable explanation
        
        Args:
            decision: Decision category
            primary_threat: Primary threat model
            model_outputs: All model outputs
            scores: All model scores
            
        Returns:
            str: Human-readable explanation
        """
        if decision == 'SAFE':
            return self._generate_safe_explanation(model_outputs, scores)
        elif decision == 'WARNING':
            return self._generate_warning_explanation(primary_threat, model_outputs, scores)
        else:  # CRITICAL
            return self._generate_critical_explanation(primary_threat, model_outputs, scores)
    
    def _generate_safe_explanation(self, model_outputs: Dict[str, Dict[str, Any]],
                                  scores: Dict[str, float]) -> str:
        """Generate explanation for SAFE decision"""
        # Find any minor concerns
        minor_concerns = [
            name for name, score in scores.items() if 0.1 < score < 0.3
        ]
        
        if minor_concerns:
            concern_name = minor_concerns[0]
            reason = model_outputs.get(concern_name, {}).get('reason', '')
            return f"All systems normal. Minor variance detected: {reason}"
        
        return "All systems normal. No security threats detected."
    
    def _generate_warning_explanation(self, primary_threat: str,
                                     model_outputs: Dict[str, Dict[str, Any]],
                                     scores: Dict[str, float]) -> str:
        """Generate explanation for WARNING decision"""
        primary_reason = model_outputs.get(primary_threat, {}).get('reason', 'Unknown')
        
        # Find supporting evidence
        supporting = [
            name for name, score in scores.items()
            if name != primary_threat and score > 0.2
        ]
        
        if supporting:
            support_name = supporting[0]
            support_reason = model_outputs.get(support_name, {}).get('reason', '')
            return f"WARNING: {primary_reason}. Supporting evidence: {support_reason}"
        
        return f"WARNING: {primary_reason}"
    
    def _generate_critical_explanation(self, primary_threat: str,
                                      model_outputs: Dict[str, Dict[str, Any]],
                                      scores: Dict[str, float]) -> str:
        """Generate explanation for CRITICAL decision"""
        primary_reason = model_outputs.get(primary_threat, {}).get('reason', 'Unknown threat')
        
        # Count high-scoring models
        high_threats = [name for name, score in scores.items() if score > 0.5]
        
        if len(high_threats) > 1:
            return f"CRITICAL: {primary_reason}. Multiple threat indicators detected ({len(high_threats)} models)"
        
        return f"CRITICAL: {primary_reason}"
    
    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update fusion weights dynamically
        
        Args:
            new_weights: New weight configuration
        """
        # Validate weights sum to 1.0
        weight_sum = sum(new_weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")
        
        self.weights.update(new_weights)
    
    def get_weights(self) -> Dict[str, float]:
        """Get current fusion weights"""
        return self.weights.copy()
    
    def reset_weights(self) -> None:
        """Reset weights to default configuration"""
        self.weights = self.config.FUSION_WEIGHTS.copy()


# Utility function for quick risk calculation
def quick_risk_calculation(anomaly: float, fdia: float, physics: float,
                          behavior: float, memory: float) -> float:
    """
    Quick risk calculation without full fusion engine
    
    Args:
        anomaly: Anomaly score
        fdia: FDIA score
        physics: Physics score
        behavior: Behavior score
        memory: Memory score
        
    Returns:
        float: Risk score
    """
    weights = AIEngineConfig.FUSION_WEIGHTS
    risk = (
        weights['anomaly'] * anomaly +
        weights['fdia'] * fdia +
        weights['physics'] * physics +
        weights['behavior'] * behavior +
        weights['memory'] * memory
    )
    return max(0.0, min(1.0, risk))
