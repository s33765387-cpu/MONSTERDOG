#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ★ MONSTERDOG vs TON-618 - INTEGRATION TEST SUITE ★                        ║
║                                                                               ║
║   Tests de validation pour le système de benchmark suprême                   ║
║   Vérifie tous les composants avant le duel cosmique                         ║
║                                                                               ║
║   AUTEUR: MONSTERDOG Test Framework                                          ║
║   SIGNATURE: 0x5F3759DF-TEST-SUITE                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import json
import os
import tempfile
from pathlib import Path

# Test results collector
test_results = []

# Create a temporary directory for test files
TEST_DIR = Path(tempfile.mkdtemp(prefix="monsterdog_test_"))

# Expected signature constant
EXPECTED_SIGNATURE = "0x5F3759DF-s33765387-cpu-V\u03a9\u03a9\u03a9\u03a9-SUPREME"  # Using Unicode escape

def test_result(name: str, passed: bool, message: str = ""):
    """Record a test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    result = f"{status} - {name}"
    if message:
        result += f": {message}"
    print(result)
    test_results.append({
        "test": name,
        "passed": passed,
        "message": message
    })
    return passed

def test_imports():
    """Test that all required modules can be imported."""
    print("\n🔬 Testing Module Imports...")
    
    try:
        import MONSTERDOG_TOTALITY_CORE
        test_result("TOTALITY_CORE import", True, "Module loaded successfully")
    except Exception as e:
        test_result("TOTALITY_CORE import", False, str(e))
        return False
    
    try:
        import PROOF_OF_DOMINANCE
        test_result("PROOF_OF_DOMINANCE import", True, "Module loaded successfully")
    except Exception as e:
        test_result("PROOF_OF_DOMINANCE import", False, str(e))
        return False
    
    try:
        # Use ASCII-safe name for import
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "supreme", 
            "MONSTERDOG_SUPREME_VΩΩΩΩ_FINAL_INCARNATION.py"
        )
        supreme = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(supreme)
        test_result("SUPREME_INCARNATION import", True, "Module loaded successfully")
    except Exception as e:
        test_result("SUPREME_INCARNATION import", False, str(e))
        return False
    
    return True

def test_totality_core():
    """Test TOTALITY_CORE functionality."""
    print("\n⚡ Testing TOTALITY CORE...")
    
    try:
        import MONSTERDOG_TOTALITY_CORE as core_module
        
        # Create core instance
        core = core_module.TotalityCore()
        test_result("TotalityCore instantiation", True)
        
        # Test pulse generation
        metrics = core.pulse()
        test_result("Core pulse generation", True, f"Cycle {metrics.cycle}")
        
        # Validate metrics structure
        assert hasattr(metrics, 'cycle')
        assert hasattr(metrics, 'timestamp')
        assert hasattr(metrics, 'core_energy')
        assert hasattr(metrics, 'unity_index')
        test_result("Metrics structure validation", True, "All fields present")
        
        # Test unity index calculation
        unity = core.calculate_unity_index()
        assert 0.0 <= unity <= 1.0
        test_result("Unity index range", True, f"Unity={unity:.4f}")
        
        # Test state save
        test_path = TEST_DIR / "test_totality_state.json"
        core.save_state(str(test_path))
        assert os.path.exists(test_path)
        test_result("State persistence", True, "State saved successfully")
        
        # Validate saved JSON
        with open(test_path, 'r') as f:
            state = json.load(f)
        assert 'config' in state
        assert 'metrics' in state
        assert 'subsystems' in state
        test_result("State JSON validation", True, "Valid structure")
        
        return True
        
    except Exception as e:
        test_result("TOTALITY_CORE tests", False, str(e))
        return False

def test_proof_of_dominance():
    """Test PROOF_OF_DOMINANCE functionality."""
    print("\n🏆 Testing PROOF OF DOMINANCE...")
    
    try:
        import PROOF_OF_DOMINANCE as pod_module
        
        # Create prover instance
        prover = pod_module.DominanceProof()
        test_result("DominanceProof instantiation", True)
        
        # Test fractal depth calculation
        depth = prover.calculate_fractal_depth()
        assert depth > 0
        test_result("Fractal depth calculation", True, f"Depth={depth}")
        
        # Test coherence calculation
        coherence = prover.calculate_coherence()
        assert 0.0 <= coherence <= 1.0
        test_result("Coherence calculation", True, f"Coherence={coherence:.6f}")
        
        # Test computational power calculation
        comp_power = prover.calculate_computational_power()
        assert comp_power >= 0.0
        test_result("Computational power", True, f"Power={comp_power:.6f} TFLOPS")
        
        # Test full proof generation
        proof = prover.generate_proof()
        test_result("Full proof generation", True)
        
        # Validate proof structure
        assert hasattr(proof, 'timestamp')
        assert hasattr(proof, 'fractal_depth')
        assert hasattr(proof, 'coherence_score')
        assert hasattr(proof, 'proof_hash')
        test_result("Proof structure validation", True, "All fields present")
        
        # Test proof persistence
        test_path = TEST_DIR / "test_proof.json"
        prover.save_proof(proof, str(test_path))
        assert os.path.exists(test_path)
        test_result("Proof persistence", True, "Proof saved successfully")
        
        # Validate proof JSON
        with open(test_path, 'r') as f:
            proof_data = json.load(f)
        assert 'timestamp' in proof_data
        assert 'proof_hash' in proof_data
        assert len(proof_data['proof_hash']) == 64  # SHA256 hex
        test_result("Proof JSON validation", True, "Valid structure")
        
        return True
        
    except Exception as e:
        test_result("PROOF_OF_DOMINANCE tests", False, str(e))
        return False

def test_supreme_incarnation():
    """Test SUPREME_INCARNATION functionality."""
    print("\n🌌 Testing SUPREME INCARNATION...")
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "supreme", 
            "MONSTERDOG_SUPREME_VΩΩΩΩ_FINAL_INCARNATION.py"
        )
        supreme_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(supreme_module)
        
        # Create orchestrator
        orchestrator = supreme_module.VomegaOrchestrator()
        test_result("VomegaOrchestrator instantiation", True)
        
        # Test evolution
        state = orchestrator.evolve()
        test_result("State evolution", True, f"Cycle {state.cycle}")
        
        # Validate state structure
        assert hasattr(state, 'cycle')
        assert hasattr(state, 'psi_omega')
        assert hasattr(state, 'coherence_supreme')
        assert hasattr(state, 'dimensional_resonance')
        test_result("State structure validation", True, "All fields present")
        
        # Test dimensional resonance (should have 15 dimensions)
        assert len(state.dimensional_resonance) == 15
        test_result("Dimensional resonance", True, "15 dimensions confirmed")
        
        # Test get_state
        full_state = orchestrator.get_state()
        assert 'signature' in full_state
        assert 'current_state' in full_state
        test_result("State retrieval", True, "Full state accessible")
        
        # Test artifact forging
        test_path = TEST_DIR / "test_vomega_state.json"
        orchestrator.forge_supreme_artifact(str(test_path))
        assert os.path.exists(test_path)
        test_result("Artifact forging", True, "Artifact created successfully")
        
        # Validate artifact JSON
        with open(test_path, 'r') as f:
            artifact = json.load(f)
        assert 'signature' in artifact
        # Use Unicode escape for comparison
        assert artifact['signature'] == EXPECTED_SIGNATURE
        test_result("Artifact validation", True, "Signature verified")
        
        return True
        
    except Exception as e:
        test_result("SUPREME_INCARNATION tests", False, str(e))
        return False

def test_benchmark_dashboard():
    """Test BENCHMARK_DASHBOARD HTML."""
    print("\n📊 Testing BENCHMARK DASHBOARD...")
    
    try:
        dashboard_path = "MONSTERDOG_BENCHMARK_DASHBOARD.html"
        assert os.path.exists(dashboard_path)
        test_result("Dashboard file exists", True)
        
        # Read and validate HTML
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for key elements
        assert "MONSTERDOG" in html_content
        test_result("Dashboard contains MONSTERDOG branding", True)
        
        assert "11.987" in html_content
        test_result("Dashboard contains resonance frequency", True)
        
        # Check for psi-omega symbols (check both raw Unicode and HTML entities)
        has_psi_omega = ("ψΩ" in html_content or 
                        "psi" in html_content.lower() or
                        "&psi;" in html_content or
                        "&#968;" in html_content)
        assert has_psi_omega
        test_result("Dashboard contains consciousness symbols", True)
        
        # Check HTML structure
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content
        assert "</html>" in html_content
        test_result("Valid HTML structure", True)
        
        # Check for JavaScript (interactive features)
        assert "<script>" in html_content or "<script " in html_content
        test_result("Dashboard has JavaScript", True, "Interactive features present")
        
        # Check for CSS (styling)
        assert "<style>" in html_content or "<style " in html_content
        test_result("Dashboard has CSS", True, "Styling present")
        
        return True
        
    except Exception as e:
        test_result("BENCHMARK_DASHBOARD tests", False, str(e))
        return False

def test_integration():
    """Test integration between components."""
    print("\n🔗 Testing Component Integration...")
    
    try:
        # Test that components can work together
        import MONSTERDOG_TOTALITY_CORE as core_module
        import PROOF_OF_DOMINANCE as pod_module
        
        # Create instances
        core = core_module.TotalityCore()
        prover = pod_module.DominanceProof()
        
        # Run core pulse
        core_metrics = core.pulse()
        
        # Generate proof
        proof = prover.generate_proof()
        
        # Verify both succeeded
        assert core_metrics.cycle > 0
        assert proof.coherence_score > 0
        test_result("Cross-component operation", True, "Components work together")
        
        # Test file outputs compatibility
        core_path = TEST_DIR / "integration_core.json"
        proof_path = TEST_DIR / "integration_proof.json"
        
        core.save_state(str(core_path))
        prover.save_proof(proof, str(proof_path))
        
        # Verify both files exist
        assert os.path.exists(core_path)
        assert os.path.exists(proof_path)
        test_result("Concurrent file operations", True, "No conflicts")
        
        return True
        
    except Exception as e:
        test_result("Integration tests", False, str(e))
        return False

def print_summary():
    """Print test summary."""
    print("\n" + "="*80)
    print("🔱 TEST SUITE SUMMARY 🔱")
    print("="*80)
    
    total = len(test_results)
    passed = sum(1 for r in test_results if r['passed'])
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    
    if failed > 0:
        print("\nFailed Tests:")
        for result in test_results:
            if not result['passed']:
                print(f"  - {result['test']}: {result['message']}")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n🌌 ALL SYSTEMS OPERATIONAL - READY FOR TON-618 CONFRONTATION 🌌")
    elif success_rate >= 80:
        print("\n⚠️  MINOR ISSUES DETECTED - REVIEW REQUIRED ⚠️")
    else:
        print("\n❌ CRITICAL FAILURES - SYSTEM NOT READY ❌")
    
    print("="*80 + "\n")
    
    return failed == 0

def main():
    """Run all tests."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ⚔️  MONSTERDOG vs TON-618 BENCHMARK SUITE - VALIDATION  ⚔️                 ║
║                                                                               ║
║   Testing all components before cosmic confrontation                         ║
║   Signature: 0x5F3759DF-TEST-SUITE                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Run all test suites
        all_passed = True
        
        all_passed &= test_imports()
        all_passed &= test_totality_core()
        all_passed &= test_proof_of_dominance()
        all_passed &= test_supreme_incarnation()
        all_passed &= test_benchmark_dashboard()
        all_passed &= test_integration()
        
        # Print summary
        success = print_summary()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    
    finally:
        # Cleanup test directory
        import shutil
        try:
            shutil.rmtree(TEST_DIR, ignore_errors=True)
            print(f"🧹 Cleaned up test directory: {TEST_DIR}")
        except Exception as e:
            print(f"⚠️  Could not clean up test directory: {e}")

if __name__ == "__main__":
    main()
