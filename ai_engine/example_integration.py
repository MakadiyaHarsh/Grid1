"""
Example Integration with Cybersecurity Gateway

This script demonstrates how to integrate the AI engine
with the cybersecurity gateway component.
"""

from ai_pipeline import analyze


class CybersecurityGateway:
    """
    Example cybersecurity gateway that uses AI engine
    for command validation
    """
    
    def __init__(self):
        self.blocked_commands = []
        self.flagged_commands = []
        self.allowed_commands = []
        
    def process_operator_command(self, command_data):
        """
        Process operator command through AI engine
        
        Args:
            command_data: Telemetry data from operator command
            
        Returns:
            dict: Processing result with status and reason
        """
        # Analyze command with AI engine
        ai_result = analyze(command_data)
        
        # Make decision based on AI output
        if ai_result['decision'] == 'CRITICAL':
            # Block command
            self.blocked_commands.append({
                'command': command_data,
                'reason': ai_result['explanation'],
                'risk': ai_result['final_risk']
            })
            
            return {
                'status': 'BLOCKED',
                'reason': ai_result['explanation'],
                'risk_score': ai_result['final_risk'],
                'confidence': ai_result['confidence']
            }
            
        elif ai_result['decision'] == 'WARNING':
            # Flag for review but allow
            self.flagged_commands.append({
                'command': command_data,
                'reason': ai_result['explanation'],
                'risk': ai_result['final_risk']
            })
            
            return {
                'status': 'FLAGGED',
                'reason': ai_result['explanation'],
                'risk_score': ai_result['final_risk'],
                'confidence': ai_result['confidence'],
                'action': 'Command allowed but flagged for review'
            }
            
        else:  # SAFE
            # Allow command
            self.allowed_commands.append({
                'command': command_data,
                'risk': ai_result['final_risk']
            })
            
            return {
                'status': 'ALLOWED',
                'risk_score': ai_result['final_risk'],
                'confidence': ai_result['confidence']
            }
    
    def get_statistics(self):
        """Get gateway statistics"""
        total = len(self.blocked_commands) + len(self.flagged_commands) + len(self.allowed_commands)
        
        return {
            'total_commands': total,
            'blocked': len(self.blocked_commands),
            'flagged': len(self.flagged_commands),
            'allowed': len(self.allowed_commands),
            'block_rate': len(self.blocked_commands) / total if total > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    gateway = CybersecurityGateway()
    
    print("="*60)
    print("CYBERSECURITY GATEWAY - AI ENGINE INTEGRATION DEMO")
    print("="*60)
    
    # Test 1: Normal command (should be allowed)
    print("\n1. Processing normal command...")
    result = gateway.process_operator_command({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 100.0,
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:00"
    })
    print(f"   Status: {result['status']}")
    print(f"   Risk: {result['risk_score']:.3f}")
    
    # Test 2: FDIA attack (should be blocked)
    print("\n2. Processing FDIA attack...")
    result = gateway.process_operator_command({
        "voltage": 1.08,
        "frequency": 50.3,
        "power_flow": 95.0,
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:05"
    })
    print(f"   Status: {result['status']}")
    print(f"   Risk: {result['risk_score']:.3f}")
    print(f"   Reason: {result['reason']}")
    
    # Test 3: Physics violation (should be blocked)
    print("\n3. Processing physics violation...")
    result = gateway.process_operator_command({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 50.0,
        "breaker_status": "OFF",
        "timestamp": "2026-01-31T10:00:10"
    })
    print(f"   Status: {result['status']}")
    print(f"   Risk: {result['risk_score']:.3f}")
    print(f"   Reason: {result['reason']}")
    
    # Statistics
    print("\n" + "="*60)
    print("GATEWAY STATISTICS")
    print("="*60)
    stats = gateway.get_statistics()
    print(f"Total Commands: {stats['total_commands']}")
    print(f"Allowed: {stats['allowed']}")
    print(f"Flagged: {stats['flagged']}")
    print(f"Blocked: {stats['blocked']}")
    print(f"Block Rate: {stats['block_rate']*100:.1f}%")
    print("="*60)
