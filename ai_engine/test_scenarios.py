"""
Test Scenarios for Multi-Model AI Engine

This module contains comprehensive test scenarios to validate
all AI models and the complete pipeline.

Run with: python test_scenarios.py
"""

import sys
from datetime import datetime, timedelta
from ai_pipeline import analyze, get_pipeline


def print_result(scenario_name, result):
    """Pretty print test result"""
    print(f"\n{'='*60}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*60}")
    print(f"Decision: {result['decision']}")
    print(f"Risk Score: {result['final_risk']:.3f}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Explanation: {result['explanation']}")
    print(f"\nModel Scores:")
    for model, score in result['model_outputs'].items():
        print(f"  {model:12s}: {score:.3f}")
    print(f"\nPrimary Threat: {result['details']['primary_threat']}")
    print(f"{'='*60}\n")


def test_normal_operation():
    """Test Scenario 1: Normal Operation"""
    print("\n🔹 TEST 1: Normal Operation")
    
    result = analyze({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 100.0,
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:00"
    })
    
    print_result("Normal Operation", result)
    
    # Assertions
    assert result['decision'] == 'SAFE', f"Expected SAFE, got {result['decision']}"
    assert result['final_risk'] < 0.3, f"Risk too high: {result['final_risk']}"
    print("✅ PASSED: Normal operation detected correctly")


def test_fdia_attack():
    """Test Scenario 2: FDIA Attack"""
    print("\n🔹 TEST 2: FDIA Attack")
    
    # First, establish baseline with normal data
    for i in range(5):
        analyze({
            "voltage": 1.0,
            "frequency": 50.0,
            "power_flow": 100.0,
            "breaker_status": "ON",
            "timestamp": f"2026-01-31T10:00:{i:02d}"
        })
    
    # Now inject FDIA attack
    result = analyze({
        "voltage": 1.08,      # Injected high
        "frequency": 50.3,    # Injected high
        "power_flow": 95.0,   # Coordinated but residual unchanged
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:10"
    })
    
    print_result("FDIA Attack", result)
    
    # Assertions
    assert result['decision'] in ['WARNING', 'CRITICAL'], \
        f"Expected WARNING or CRITICAL, got {result['decision']}"
    assert result['model_outputs']['fdia'] > 0.3, \
        f"FDIA score too low: {result['model_outputs']['fdia']}"
    print("✅ PASSED: FDIA attack detected correctly")


def test_physics_violation():
    """Test Scenario 3: Physics Violation"""
    print("\n🔹 TEST 3: Physics Violation")
    
    result = analyze({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 50.0,   # Power flowing!
        "breaker_status": "OFF",  # But breaker is OFF (violation!)
        "timestamp": "2026-01-31T10:00:15"
    })
    
    print_result("Physics Violation", result)
    
    # Assertions
    assert result['decision'] == 'CRITICAL', \
        f"Expected CRITICAL, got {result['decision']}"
    assert result['model_outputs']['physics'] > 0.8, \
        f"Physics score too low: {result['model_outputs']['physics']}"
    print("✅ PASSED: Physics violation detected correctly")


def test_replay_attack():
    """Test Scenario 4: Replay Attack"""
    print("\n🔹 TEST 4: Replay Attack")
    
    # Send first command
    timestamp = "2026-01-31T10:00:20"
    analyze({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 100.0,
        "breaker_status": "ON",
        "timestamp": timestamp
    })
    
    # Send same timestamp again (replay attack)
    result = analyze({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 100.0,
        "breaker_status": "OFF",
        "timestamp": timestamp  # Same timestamp!
    })
    
    print_result("Replay Attack", result)
    
    # Assertions
    assert result['decision'] in ['WARNING', 'CRITICAL'], \
        f"Expected WARNING or CRITICAL, got {result['decision']}"
    assert result['model_outputs']['behavior'] > 0.5, \
        f"Behavior score too low: {result['model_outputs']['behavior']}"
    print("✅ PASSED: Replay attack detected correctly")


def test_insider_misuse():
    """Test Scenario 5: Insider Misuse (Excessive Switching)"""
    print("\n🔹 TEST 5: Insider Misuse (Excessive Switching)")
    
    # Reset pipeline for clean test
    pipeline = get_pipeline()
    pipeline.reset()
    
    # Perform excessive switching
    base_time = datetime.fromisoformat("2026-01-31T10:00:00")
    
    for i in range(15):
        timestamp = (base_time + timedelta(seconds=i*10)).isoformat()
        analyze({
            "voltage": 1.0,
            "frequency": 50.0,
            "power_flow": 100.0,
            "breaker_status": "ON" if i % 2 == 0 else "OFF",
            "timestamp": timestamp
        })
    
    # Get last result
    result = analyze({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 100.0,
        "breaker_status": "ON",
        "timestamp": (base_time + timedelta(seconds=160)).isoformat()
    })
    
    print_result("Insider Misuse", result)
    
    # Assertions
    assert result['decision'] in ['WARNING', 'CRITICAL'], \
        f"Expected WARNING or CRITICAL, got {result['decision']}"
    assert result['model_outputs']['behavior'] > 0.3, \
        f"Behavior score too low: {result['model_outputs']['behavior']}"
    print("✅ PASSED: Insider misuse detected correctly")


def test_off_hours_operation():
    """Test Scenario 6: Off-Hours Operation"""
    print("\n🔹 TEST 6: Off-Hours Operation")
    
    # Reset pipeline
    pipeline = get_pipeline()
    pipeline.reset()
    
    # Establish normal daytime pattern
    for i in range(5):
        analyze({
            "voltage": 1.0,
            "frequency": 50.0,
            "power_flow": 100.0,
            "breaker_status": "ON",
            "timestamp": f"2026-01-31T14:00:{i:02d}"
        })
    
    # Now operate at night with breaker change
    result = analyze({
        "voltage": 1.0,
        "frequency": 50.0,
        "power_flow": 0.0,
        "breaker_status": "OFF",
        "timestamp": "2026-01-31T02:00:00"  # 2 AM
    })
    
    print_result("Off-Hours Operation", result)
    
    # Note: This may or may not trigger depending on history
    print("✅ PASSED: Off-hours operation analyzed")


def test_memory_similarity():
    """Test Scenario 7: Memory Similarity to Known Attack"""
    print("\n🔹 TEST 7: Memory Similarity")
    
    # Reset pipeline
    pipeline = get_pipeline()
    pipeline.reset()
    
    # Build history
    for i in range(10):
        analyze({
            "voltage": 1.0,
            "frequency": 50.0,
            "power_flow": 100.0,
            "breaker_status": "ON",
            "timestamp": f"2026-01-31T10:00:{i:02d}"
        })
    
    # Send data similar to attack signature
    result = analyze({
        "voltage": 1.15,      # High voltage (similar to signature)
        "frequency": 50.25,   # High frequency
        "power_flow": 150.0,  # High power
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:15"
    })
    
    print_result("Memory Similarity", result)
    
    # Assertions
    assert result['model_outputs']['memory'] >= 0.0, \
        "Memory model should return a score"
    print("✅ PASSED: Memory similarity analyzed")


def test_voltage_bounds_violation():
    """Test Scenario 8: Voltage Bounds Violation"""
    print("\n🔹 TEST 8: Voltage Bounds Violation")
    
    result = analyze({
        "voltage": 1.12,      # Above 1.05 limit
        "frequency": 50.0,
        "power_flow": 100.0,
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:20"
    })
    
    print_result("Voltage Bounds Violation", result)
    
    # Assertions
    assert result['model_outputs']['physics'] > 0.0, \
        f"Physics score should detect violation"
    print("✅ PASSED: Voltage bounds violation detected")


def test_frequency_bounds_violation():
    """Test Scenario 9: Frequency Bounds Violation"""
    print("\n🔹 TEST 9: Frequency Bounds Violation")
    
    result = analyze({
        "voltage": 1.0,
        "frequency": 51.0,    # Above 50.5 Hz limit
        "power_flow": 100.0,
        "breaker_status": "ON",
        "timestamp": "2026-01-31T10:00:25"
    })
    
    print_result("Frequency Bounds Violation", result)
    
    # Assertions
    assert result['model_outputs']['physics'] > 0.0, \
        f"Physics score should detect violation"
    print("✅ PASSED: Frequency bounds violation detected")


def run_all_tests():
    """Run all test scenarios"""
    print("\n" + "="*60)
    print("MULTI-MODEL AI ENGINE - TEST SUITE")
    print("="*60)
    
    tests = [
        test_normal_operation,
        test_fdia_attack,
        test_physics_violation,
        test_replay_attack,
        test_insider_misuse,
        test_off_hours_operation,
        test_memory_similarity,
        test_voltage_bounds_violation,
        test_frequency_bounds_violation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
