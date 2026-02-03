"""
AI Interface Module
===================
Clean interface between Cybersecurity Gateway and Multi-Model AI Engine.

This module:
- Converts gateway telemetry format to AI engine format
- Invokes AI pipeline analysis
- Handles AI errors gracefully
- Logs AI analysis results
"""

import sys
import os
import logging
from datetime import datetime
from typing import Dict, Any

# Add ai_engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_engine'))

try:
    from ai_pipeline import analyze
    AI_AVAILABLE = True
except ImportError as e:
    AI_AVAILABLE = False
    AI_IMPORT_ERROR = str(e)

# Configure AI logging
AI_LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'ai.log')
os.makedirs(os.path.dirname(AI_LOG_PATH), exist_ok=True)

ai_logger = logging.getLogger('ai_interface')
ai_logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(AI_LOG_PATH)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
ai_logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[AI] %(message)s'))
ai_logger.addHandler(console_handler)


def analyze_with_ai(grid_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze grid telemetry using Multi-Model AI Engine
    
    Args:
        grid_data: Current grid state from grid simulator
            {
                "voltage": float,        # Per-unit voltage
                "frequency": float,      # Frequency in Hz
                "power_flow": float,     # Power flow in MW
                "breaker": str          # "ON" or "OFF"
            }
    
    Returns:
        dict: AI analysis result
            {
                "decision": str,         # "SAFE", "WARNING", or "CRITICAL"
                "risk_score": float,     # 0.0 to 1.0
                "explanation": str,      # Human-readable explanation
                "model_outputs": dict,   # Individual model scores
                "confidence": float      # Confidence in decision
            }
    """
    
    # Check if AI engine is available
    if not AI_AVAILABLE:
        ai_logger.warning(f"AI Engine not available: {AI_IMPORT_ERROR}")
        return {
            "decision": "SAFE",
            "risk_score": 0.0,
            "explanation": "AI engine unavailable - using fallback",
            "model_outputs": {},
            "confidence": 0.0,
            "error": AI_IMPORT_ERROR
        }
    
    try:
        # Convert gateway format to AI format
        ai_input = {
            "voltage": grid_data.get("voltage", 1.0),
            "frequency": grid_data.get("frequency", 50.0),
            "power_flow": grid_data.get("power_flow", 0.0),
            "breaker_status": grid_data.get("breaker", "OFF"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Invoke AI pipeline
        ai_result = analyze(ai_input)
        
        # Extract key information
        decision = ai_result.get("decision", "SAFE")
        risk_score = ai_result.get("final_risk", 0.0)
        explanation = ai_result.get("explanation", "No explanation provided")
        model_outputs = ai_result.get("model_outputs", {})
        confidence = ai_result.get("confidence", 0.0)
        
        # Log AI analysis
        ai_logger.info(f"AI RISK {risk_score:.2f} — {decision}")
        ai_logger.info(f"EXPLANATION: {explanation}")
        ai_logger.info(f"MODEL OUTPUTS: Anomaly={model_outputs.get('anomaly', 0):.2f}, "
                      f"FDIA={model_outputs.get('fdia', 0):.2f}, "
                      f"Physics={model_outputs.get('physics', 0):.2f}, "
                      f"Behavior={model_outputs.get('behavior', 0):.2f}, "
                      f"Memory={model_outputs.get('memory', 0):.2f}")
        
        # Return formatted result
        return {
            "decision": decision,
            "risk_score": risk_score,
            "explanation": explanation,
            "model_outputs": model_outputs,
            "confidence": confidence,
            "details": ai_result.get("details", {})
        }
        
    except Exception as e:
        # Handle AI errors gracefully
        ai_logger.error(f"AI ANALYSIS ERROR: {str(e)}")
        return {
            "decision": "SAFE",
            "risk_score": 0.0,
            "explanation": f"AI analysis failed: {str(e)}",
            "model_outputs": {},
            "confidence": 0.0,
            "error": str(e)
        }


def get_ai_status() -> Dict[str, Any]:
    """
    Get AI engine status
    
    Returns:
        dict: AI engine status information
    """
    return {
        "available": AI_AVAILABLE,
        "error": AI_IMPORT_ERROR if not AI_AVAILABLE else None,
        "log_path": AI_LOG_PATH
    }


# Test function
if __name__ == "__main__":
    print("=" * 60)
    print("AI INTERFACE MODULE TEST")
    print("=" * 60)
    
    # Check status
    status = get_ai_status()
    print(f"\nAI Engine Available: {status['available']}")
    if not status['available']:
        print(f"Error: {status['error']}")
    
    # Test analysis
    test_data = {
        "voltage": 1.02,
        "frequency": 50.1,
        "power_flow": 102.0,
        "breaker": "ON"
    }
    
    print(f"\nTest Input: {test_data}")
    result = analyze_with_ai(test_data)
    print(f"\nAI Decision: {result['decision']}")
    print(f"Risk Score: {result['risk_score']:.2f}")
    print(f"Explanation: {result['explanation']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print("\n" + "=" * 60)
