"""
Cybersecurity Gateway - Main Server
Industrial-grade security layer for AI-Driven Cyber-Physical Power Grid Protection Platform
"""

from flask import Flask, request, jsonify
import uuid
import datetime
import config
from logger import SecurityLogger
from rules_engine import CyberRulesEngine
from attack_detector import AttackDetector
from forwarder import GridForwarder
from ai_interface import analyze_with_ai, get_ai_status

# Initialize Flask app
app = Flask(__name__)

# Initialize components
logger = SecurityLogger(enable_color=config.ENABLE_COLOR_LOGS)
rules_engine = CyberRulesEngine()
attack_detector = AttackDetector()
grid_forwarder = GridForwarder()

@app.route('/', methods=['GET'])
def home():
    """Gateway status endpoint"""
    return jsonify({
        "service": "Cybersecurity Gateway",
        "status": "operational",
        "version": "1.0.0",
        "description": "Industrial-grade security layer for power grid protection",
        "endpoints": {
            "operator_command": "POST /operator/command"
        }
    })

@app.route('/operator/command', methods=['POST'])
def operator_command():
    """
    Main endpoint for operator commands
    All commands must pass through this security gateway
    """
    
    # Generate request ID and timestamp
    request_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.now()
    
    # Get command from request
    try:
        command = request.get_json()
        if command is None:
            return jsonify({
                "status": "BLOCKED",
                "decision_layer": "Cybersecurity Gateway",
                "attack_type": "MALFORMED_REQUEST",
                "risk_score": 1.0,
                "reason": "Invalid JSON or missing request body"
            }), 400
    except Exception as e:
        return jsonify({
            "status": "BLOCKED",
            "decision_layer": "Cybersecurity Gateway",
            "attack_type": "MALFORMED_REQUEST",
            "risk_score": 1.0,
            "reason": f"Failed to parse request: {str(e)}"
        }), 400
    
    logger.log_info(f"[{request_id}] OPERATOR COMMAND RECEIVED: {command}")
    
    # STEP 1: Cyber Rules Validation
    logger.log_info(f"[{request_id}] Running cyber rules validation...")
    rules_result = rules_engine.validate_command(command)
    
    if rules_result["status"] == "BLOCKED":
        logger.log_warning(f"[{request_id}] CYBER RULES FAILED: {rules_result['reason']}")
    else:
        logger.log_info(f"[{request_id}] CYBER RULES PASSED")
    
    # STEP 2: Attack Detection
    logger.log_info(f"[{request_id}] Running attack detection analysis...")
    attack_result = attack_detector.analyze_command(command)
    
    logger.log_info(f"[{request_id}] ATTACK DETECTION: {attack_result['attack_type']}")
    logger.log_info(f"[{request_id}] ANOMALY SCORE: {attack_result['anomaly_score']:.2f}")
    
    # STEP 3: AI Analysis
    logger.log_info(f"[{request_id}] Running AI multi-model analysis...")
    # Fetch current grid telemetry for AI analysis
    grid_telemetry = grid_forwarder.get_grid_telemetry()
    ai_result = analyze_with_ai(grid_telemetry)
    
    logger.log_info(f"[{request_id}] AI DECISION: {ai_result['decision']}")
    logger.log_info(f"[{request_id}] AI RISK SCORE: {ai_result['risk_score']:.2f}")
    logger.log_info(f"[{request_id}] AI EXPLANATION: {ai_result['explanation']}")
    
    # STEP 4: Security Decision Engine
    # Combine risk scores (traditional + AI)
    combined_risk = max(
        rules_result["risk_level"], 
        attack_result["anomaly_score"],
        ai_result["risk_score"] * config.AI_RISK_WEIGHT
    )
    
    logger.log_info(f"[{request_id}] COMBINED RISK SCORE: {combined_risk:.2f}")
    logger.log_info(f"[{request_id}] RISK THRESHOLD: {config.RISK_THRESHOLD}")
    
    # Make decision (consider AI decision for CRITICAL threats)
    ai_blocks = ai_result["decision"] == "CRITICAL"
    
    if combined_risk > config.RISK_THRESHOLD or rules_result["status"] == "BLOCKED" or ai_blocks:
        decision = "BLOCKED"
        
        # Determine primary reason
        if rules_result["status"] == "BLOCKED":
            reason = rules_result["reason"]
        elif ai_blocks:
            reason = f"AI CRITICAL: {ai_result['explanation']}"
        else:
            reason = f"{attack_result['attack_type']}: {attack_result['details']}"
        
        logger.log_warning(f"[{request_id}] DECISION: BLOCKED")
        logger.log_warning(f"[{request_id}] REASON: {reason}")
        logger.log_info(f"[{request_id}] GRID NOT CONTACTED")
        
        # Log security event
        logger.log_event(
            request_id=request_id,
            source="Operator System",
            command=command,
            decision=decision,
            attack_type=attack_result["attack_type"],
            risk_score=combined_risk,
            reason=reason
        )
        
        # Return blocked response with AI details
        return jsonify({
            "status": "BLOCKED",
            "decision_layer": "Cybersecurity Gateway + AI Engine",
            "attack_type": attack_result["attack_type"],
            "risk_score": combined_risk,
            "reason": reason,
            "details": attack_result["details"],
            "ai_analysis": {
                "decision": ai_result["decision"],
                "risk_score": ai_result["risk_score"],
                "explanation": ai_result["explanation"],
                "confidence": ai_result["confidence"]
            },
            "request_id": request_id,
            "timestamp": timestamp.isoformat()
        }), 403
    
    else:
        decision = "ALLOWED"
        
        decision = "ALLOWED"
        
        logger.log_info(f"[{request_id}] DECISION: ALLOWED")
        if ai_result["decision"] == "WARNING":
            logger.log_warning(f"[{request_id}] AI WARNING: {ai_result['explanation']}")
        logger.log_info(f"[{request_id}] FORWARDING TO GRID...")
        
        # STEP 5: Forward to Grid
        forward_result = grid_forwarder.forward_command(command)
        
        if forward_result["success"]:
            logger.log_info(f"[{request_id}] GRID RESPONSE RECEIVED")
            
            # Log security event
            logger.log_event(
                request_id=request_id,
                source="Operator System",
                command=command,
                decision=decision,
                attack_type=attack_result["attack_type"],
                risk_score=combined_risk,
                grid_response=forward_result["response"]
            )
            
            # Return allowed response with grid data and AI analysis
            return jsonify({
                "status": "ALLOWED",
                "decision_layer": "Cybersecurity Gateway + AI Engine",
                "attack_type": attack_result["attack_type"],
                "risk_score": combined_risk,
                "grid_response": forward_result["response"],
                "ai_analysis": {
                    "decision": ai_result["decision"],
                    "risk_score": ai_result["risk_score"],
                    "explanation": ai_result["explanation"],
                    "confidence": ai_result["confidence"]
                },
                "request_id": request_id,
                "timestamp": timestamp.isoformat()
            }), 200
        
        else:
            logger.log_error(f"[{request_id}] GRID COMMUNICATION FAILED: {forward_result['error']}")
            
            # Log security event
            logger.log_event(
                request_id=request_id,
                source="Operator System",
                command=command,
                decision="ALLOWED_BUT_GRID_ERROR",
                attack_type=attack_result["attack_type"],
                risk_score=combined_risk,
                reason=forward_result["error"]
            )
            
            # Return error response
            return jsonify({
                "status": "ALLOWED",
                "decision_layer": "Cybersecurity Gateway",
                "attack_type": attack_result["attack_type"],
                "risk_score": combined_risk,
                "grid_error": forward_result["error"],
                "reason": "Command passed security checks but grid communication failed",
                "request_id": request_id,
                "timestamp": timestamp.isoformat()
            }), 502

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    grid_healthy = grid_forwarder.check_grid_health()
    
    return jsonify({
        "gateway": "healthy",
        "grid_connection": "healthy" if grid_healthy else "unreachable",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 80)
    print("CYBERSECURITY GATEWAY FOR POWER GRID SYSTEM")
    print("=" * 80)
    print(f"Gateway Server: http://{config.GATEWAY_HOST}:{config.GATEWAY_PORT}")
    print(f"Grid Simulator: {config.GRID_BASE_URL}")
    print(f"Risk Threshold: {config.RISK_THRESHOLD}")
    print("=" * 80)
    print()
    
    logger.log_info("Cybersecurity Gateway starting...")
    logger.log_info(f"Operator endpoint: POST /operator/command")
    logger.log_info(f"Grid target: {config.GRID_BASE_URL}")
    
    # Check grid connection
    if grid_forwarder.check_grid_health():
        logger.log_info("Grid simulator connection: HEALTHY")
    else:
        logger.log_warning(f"Grid simulator connection: UNREACHABLE at {config.GRID_BASE_URL}")
        logger.log_warning("Commands will be validated but forwarding will fail")
    
    print()
    logger.log_info("Gateway is OPERATIONAL and ready to receive commands")
    print()
    
    # Start Flask server
    app.run(
        host=config.GATEWAY_HOST,
        port=config.GATEWAY_PORT,
        debug=False
    )
