"""
Behavioral Pattern Learning Model (MODEL-4)

Purpose:
    Learn operator behavior patterns and detect anomalies
    
Learns:
    - Operator command timing (normal operation hours)
    - Frequency of switching (breaker toggles per hour)
    - Repetitive behavior patterns
    
Detects:
    - Replay attacks (repeated timestamps)
    - Automation abuse (excessive switching)
    - Insider anomalies (off-hours operations)

Output:
    - behavior_score ∈ [0,1]
    - confidence score
    - human-readable reason
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime
from ai_config import AIEngineConfig


class BehaviorLearningModel:
    """Learns operator behavior patterns and detects anomalies"""
    
    def __init__(self):
        self.config = AIEngineConfig.BEHAVIOR_CONFIG
        self.name = "Behavioral Pattern Learning"
        self.command_history: List[Dict[str, Any]] = []
        self.timestamp_history: List[float] = []
        self.switch_count = 0
        self.switch_timestamps: List[float] = []
        
    def analyze(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze operator behavior patterns
        
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
        behavior_scores = []
        behavior_reasons = []
        
        # Check 1: Replay Attack Detection (repeated timestamps)
        score, reason = self._check_replay_attack(preprocessed_data)
        if score > 0:
            behavior_scores.append(score)
            behavior_reasons.append(reason)
        
        # Check 2: Off-Hours Operation
        score, reason = self._check_off_hours_operation(preprocessed_data)
        if score > 0:
            behavior_scores.append(score)
            behavior_reasons.append(reason)
        
        # Check 3: Excessive Switching
        score, reason = self._check_excessive_switching(preprocessed_data)
        if score > 0:
            behavior_scores.append(score)
            behavior_reasons.append(reason)
        
        # Check 4: Rapid Command Sequence
        score, reason = self._check_rapid_commands(preprocessed_data)
        if score > 0:
            behavior_scores.append(score)
            behavior_reasons.append(reason)
        
        # Update history
        self._update_history(preprocessed_data)
        
        # Aggregate results
        if not behavior_scores:
            return {
                'score': 0.0,
                'confidence': 0.75,
                'reason': 'Normal operator behavior pattern',
                'details': {
                    'checks_performed': 4,
                    'anomalies_found': 0
                }
            }
        
        # Calculate final behavior score (max of indicators)
        final_score = max(behavior_scores)
        
        # Confidence based on number of anomalies
        confidence = min(0.90, 0.65 + (len(behavior_scores) * 0.1))
        
        # Primary reason
        primary_reason = behavior_reasons[0]
        if len(behavior_reasons) > 1:
            primary_reason += f" (+{len(behavior_reasons)-1} more anomalies)"
        
        return {
            'score': final_score,
            'confidence': confidence,
            'reason': primary_reason,
            'details': {
                'checks_performed': 4,
                'anomalies_found': len(behavior_scores),
                'all_reasons': behavior_reasons
            }
        }
    
    def _check_replay_attack(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Detect replay attacks through repeated timestamps
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        current_timestamp = data.get('timestamp_unix', 0)
        tolerance = self.config['replay_time_tolerance']
        
        # Check if this timestamp was seen before
        for past_timestamp in self.timestamp_history:
            time_diff = abs(current_timestamp - past_timestamp)
            if time_diff < tolerance:
                score = 0.9
                reason = "Replay attack detected (repeated timestamp)"
                return score, reason
        
        return 0.0, ""
    
    def _check_off_hours_operation(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Detect operations during unusual hours
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        hour = data.get('hour', 12)
        is_night = data.get('is_night', False)
        is_weekend = data.get('is_weekend', False)
        
        normal_start, normal_end = self.config['normal_hours']
        
        # Check if breaker changed during off-hours
        breaker_changed = data.get('breaker_changed', False)
        
        if breaker_changed:
            if is_night:
                score = 0.5
                reason = f"Breaker operation during night hours ({hour}:00)"
                return score, reason
            
            if is_weekend:
                score = 0.4
                reason = "Breaker operation during weekend"
                return score, reason
        
        return 0.0, ""
    
    def _check_excessive_switching(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Detect excessive breaker switching (automation abuse)
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        breaker_changed = data.get('breaker_changed', False)
        current_time = data.get('timestamp_unix', 0)
        
        if breaker_changed:
            self.switch_timestamps.append(current_time)
        
        # Count switches in last hour
        one_hour_ago = current_time - 3600
        recent_switches = [t for t in self.switch_timestamps if t > one_hour_ago]
        self.switch_timestamps = recent_switches  # Clean up old timestamps
        
        max_switches = self.config['max_switches_per_hour']
        
        if len(recent_switches) > max_switches:
            score = min(1.0, len(recent_switches) / (max_switches * 2))
            reason = f"Excessive breaker toggling ({len(recent_switches)} switches in 1 hour)"
            return score, reason
        
        return 0.0, ""
    
    def _check_rapid_commands(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Detect commands issued too rapidly (automation/script)
        
        Args:
            data: Telemetry data
            
        Returns:
            tuple: (score, reason)
        """
        delta_time = data.get('delta_time', 10.0)
        breaker_changed = data.get('breaker_changed', False)
        min_interval = self.config['command_interval_min']
        
        if breaker_changed and delta_time < min_interval:
            score = 0.6
            reason = f"Rapid command sequence ({delta_time:.1f}s interval, min {min_interval}s)"
            return score, reason
        
        return 0.0, ""
    
    def _update_history(self, data: Dict[str, Any]) -> None:
        """
        Update command history for pattern learning
        
        Args:
            data: Telemetry data
        """
        # Store command pattern
        self.command_history.append({
            'timestamp': data.get('timestamp_unix', 0),
            'hour': data.get('hour', 0),
            'breaker_status': data.get('breaker_status', 'OFF'),
            'breaker_changed': data.get('breaker_changed', False)
        })
        
        # Store timestamp for replay detection
        current_timestamp = data.get('timestamp_unix', 0)
        self.timestamp_history.append(current_timestamp)
        
        # Keep only recent history
        max_history = self.config['pattern_memory_size']
        if len(self.command_history) > max_history:
            self.command_history.pop(0)
        if len(self.timestamp_history) > max_history:
            self.timestamp_history.pop(0)
    
    def get_behavior_profile(self) -> Dict[str, Any]:
        """
        Get learned behavior profile
        
        Returns:
            dict: Behavior profile statistics
        """
        if not self.command_history:
            return {
                'total_commands': 0,
                'total_switches': 0,
                'common_hours': []
            }
        
        # Analyze command patterns
        total_commands = len(self.command_history)
        total_switches = sum(1 for c in self.command_history if c['breaker_changed'])
        
        # Find common operation hours
        hours = [c['hour'] for c in self.command_history]
        hour_counts = {}
        for h in hours:
            hour_counts[h] = hour_counts.get(h, 0) + 1
        
        common_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_commands': total_commands,
            'total_switches': total_switches,
            'common_hours': [h for h, _ in common_hours],
            'average_switches_per_hour': total_switches / max(1, total_commands / 60)
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        return {
            'name': self.name,
            'type': 'behavioral_learning',
            'methods': [
                'replay_attack_detection',
                'off_hours_detection',
                'excessive_switching_detection',
                'rapid_command_detection'
            ],
            'config': self.config
        }
