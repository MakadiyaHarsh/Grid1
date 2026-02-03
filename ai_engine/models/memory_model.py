"""
Memory & Similarity Model (MODEL-5)

Purpose:
    Maintain historical memory and detect similarity to known attack patterns
    
Maintains:
    - Last N telemetry points (historical memory)
    - Known attack signatures
    - Malicious pattern database
    
Computes:
    - Cosine similarity with historical data
    - Pattern matching with known attacks
    
Output:
    - memory_score ∈ [0,1]
    - confidence score
    - human-readable reason
"""

from typing import Dict, Any, List, Tuple
import math
from ai_config import AIEngineConfig


class MemoryModel:
    """Maintains historical memory and performs similarity analysis"""
    
    def __init__(self):
        self.config = AIEngineConfig.MEMORY_CONFIG
        self.name = "Memory & Similarity"
        self.telemetry_memory: List[Dict[str, float]] = []
        self.attack_signatures: List[Dict[str, Any]] = []
        self._initialize_attack_signatures()
        
    def analyze(self, preprocessed_data: Dict[str, Any],
                telemetry_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze similarity to historical patterns and known attacks
        
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
        # Update memory
        self._update_memory(preprocessed_data)
        
        memory_scores = []
        memory_reasons = []
        
        # Check 1: Similarity to known attack signatures
        score, reason = self._check_attack_signatures(preprocessed_data)
        if score > 0:
            memory_scores.append(score)
            memory_reasons.append(reason)
        
        # Check 2: Anomalous pattern repetition
        score, reason = self._check_pattern_repetition(preprocessed_data, telemetry_history)
        if score > 0:
            memory_scores.append(score)
            memory_reasons.append(reason)
        
        # Check 3: Sudden deviation from learned baseline
        score, reason = self._check_baseline_deviation(preprocessed_data)
        if score > 0:
            memory_scores.append(score)
            memory_reasons.append(reason)
        
        # Aggregate results
        if not memory_scores:
            return {
                'score': 0.0,
                'confidence': 0.80,
                'reason': 'No similarity to known attack patterns',
                'details': {
                    'checks_performed': 3,
                    'matches_found': 0,
                    'memory_size': len(self.telemetry_memory)
                }
            }
        
        # Calculate final memory score (max of indicators)
        final_score = max(memory_scores)
        
        # Confidence based on memory size and matches
        confidence = min(0.95, 0.70 + (len(self.telemetry_memory) / 100) * 0.2)
        
        # Primary reason
        primary_reason = memory_reasons[0]
        
        return {
            'score': final_score,
            'confidence': confidence,
            'reason': primary_reason,
            'details': {
                'checks_performed': 3,
                'matches_found': len(memory_scores),
                'all_reasons': memory_reasons,
                'memory_size': len(self.telemetry_memory)
            }
        }
    
    def _check_attack_signatures(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check similarity to known attack signatures
        
        Args:
            data: Current telemetry
            
        Returns:
            tuple: (score, reason)
        """
        current_vector = self._create_feature_vector(data)
        
        for signature in self.attack_signatures:
            signature_vector = signature['vector']
            similarity = self._cosine_similarity(current_vector, signature_vector)
            
            threshold = self.config['similarity_threshold']
            
            if similarity > threshold:
                score = similarity
                reason = f"High similarity to {signature['name']} ({similarity:.2f})"
                return score, reason
        
        return 0.0, ""
    
    def _check_pattern_repetition(self, data: Dict[str, Any],
                                  history: List[Dict[str, Any]]) -> Tuple[float, str]:
        """
        Check for anomalous pattern repetition
        
        Args:
            data: Current telemetry
            history: Historical data
            
        Returns:
            tuple: (score, reason)
        """
        if len(history) < 10:
            return 0.0, ""
        
        current_vector = self._create_feature_vector(data)
        
        # Check similarity to recent history
        high_similarity_count = 0
        for historical_data in history[-20:]:
            hist_vector = self._create_feature_vector(historical_data)
            similarity = self._cosine_similarity(current_vector, hist_vector)
            
            # Very high similarity (>0.98) might indicate replay or pattern repetition
            if similarity > 0.98:
                high_similarity_count += 1
        
        if high_similarity_count > 3:
            score = min(1.0, high_similarity_count / 10)
            reason = f"Suspicious pattern repetition detected ({high_similarity_count} matches)"
            return score, reason
        
        return 0.0, ""
    
    def _check_baseline_deviation(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Check deviation from learned baseline
        
        Args:
            data: Current telemetry
            
        Returns:
            tuple: (score, reason)
        """
        if len(self.telemetry_memory) < 20:
            return 0.0, ""
        
        # Compute baseline (average of historical memory)
        baseline = self._compute_baseline()
        current_vector = self._create_feature_vector(data)
        
        # Compute distance from baseline
        distance = self._euclidean_distance(current_vector, baseline)
        
        # Normalize distance (typical distance is ~0.1-0.3)
        normalized_distance = min(1.0, distance / 0.5)
        
        if normalized_distance > 0.6:
            score = normalized_distance
            reason = f"Significant deviation from learned baseline ({distance:.3f})"
            return score, reason
        
        return 0.0, ""
    
    def _create_feature_vector(self, data: Dict[str, Any]) -> List[float]:
        """
        Create feature vector from telemetry data
        
        Args:
            data: Telemetry data
            
        Returns:
            list: Feature vector
        """
        weights = self.config['feature_weights']
        
        # Normalize and weight features
        voltage = data.get('voltage', 1.0) * weights['voltage']
        frequency = data.get('frequency', 50.0) / 50.0 * weights['frequency']
        power = data.get('power_flow', 0.0) / 100.0 * weights['power_flow']
        
        return [voltage, frequency, power]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            float: Cosine similarity [0, 1]
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _euclidean_distance(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute Euclidean distance between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            float: Euclidean distance
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
    
    def _compute_baseline(self) -> List[float]:
        """
        Compute baseline feature vector from memory
        
        Returns:
            list: Baseline feature vector
        """
        if not self.telemetry_memory:
            return [0.3, 1.0, 0.0]  # Default baseline
        
        # Average of all memory vectors
        n = len(self.telemetry_memory)
        baseline = [0.0, 0.0, 0.0]
        
        for mem in self.telemetry_memory:
            vec = self._create_feature_vector(mem)
            for i in range(len(vec)):
                baseline[i] += vec[i]
        
        return [b / n for b in baseline]
    
    def _update_memory(self, data: Dict[str, Any]) -> None:
        """
        Update telemetry memory
        
        Args:
            data: Current telemetry
        """
        self.telemetry_memory.append({
            'voltage': data.get('voltage', 1.0),
            'frequency': data.get('frequency', 50.0),
            'power_flow': data.get('power_flow', 0.0)
        })
        
        # Keep only recent memory
        max_size = self.config['history_size']
        if len(self.telemetry_memory) > max_size:
            self.telemetry_memory.pop(0)
    
    def _initialize_attack_signatures(self) -> None:
        """Initialize known attack signatures"""
        # Signature 1: FDIA with coordinated voltage-frequency injection
        self.attack_signatures.append({
            'name': 'FDIA coordinated injection',
            'vector': [0.35, 1.05, 0.45],  # High V, high f, high P
            'description': 'Coordinated false data injection attack'
        })
        
        # Signature 2: Voltage manipulation attack
        self.attack_signatures.append({
            'name': 'Voltage manipulation',
            'vector': [0.45, 1.0, 0.3],  # Very high V, normal f, moderate P
            'description': 'Isolated voltage data manipulation'
        })
        
        # Signature 3: Zero-day attack pattern (learned from previous incidents)
        self.attack_signatures.append({
            'name': 'Zero-day pattern',
            'vector': [0.25, 0.95, 0.5],  # Low V, low f, high P (impossible)
            'description': 'Previously observed zero-day attack'
        })
    
    def add_attack_signature(self, name: str, voltage: float, frequency: float,
                           power_flow: float, description: str = "") -> None:
        """
        Add a new attack signature to the database
        
        Args:
            name: Attack name
            voltage: Voltage value
            frequency: Frequency value
            power_flow: Power flow value
            description: Attack description
        """
        vector = self._create_feature_vector({
            'voltage': voltage,
            'frequency': frequency,
            'power_flow': power_flow
        })
        
        self.attack_signatures.append({
            'name': name,
            'vector': vector,
            'description': description
        })
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics
        
        Returns:
            dict: Memory statistics
        """
        return {
            'memory_size': len(self.telemetry_memory),
            'attack_signatures': len(self.attack_signatures),
            'baseline': self._compute_baseline() if self.telemetry_memory else None
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        return {
            'name': self.name,
            'type': 'memory_similarity',
            'methods': [
                'attack_signature_matching',
                'pattern_repetition_detection',
                'baseline_deviation_analysis'
            ],
            'config': self.config,
            'signatures_loaded': len(self.attack_signatures)
        }
