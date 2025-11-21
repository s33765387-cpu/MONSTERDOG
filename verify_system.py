#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONSTERDOG Framework vΩ - System Verification Script
Tests all components without starting the web server.
"""

import asyncio
import sys
from monsterdog.core import MonsterDogQuantumCore
from monsterdog.agents import AgenticSystem, PivotMode
from monsterdog.hardware import MonsterDogHardwareMonitor
from monsterdog.security import AegisSecurity
from monsterdog.orchestrator import app


def test_security():
    """Test AEGIS Security Module."""
    print("\n🔐 Testing AEGIS Security...")
    aegis = AegisSecurity()
    
    # Generate token
    token = aegis.generate_token()
    print(f"  ✓ Token generated: {token[:16]}...")
    
    # Verify token
    if aegis.verify(token):
        print(f"  ✓ Token verification: PASSED")
    else:
        print(f"  ✗ Token verification: FAILED")
        return False
    
    # Check session info
    info = aegis.get_session_info()
    print(f"  ✓ Session active for {info['session_duration']:.2f}s")
    return True


def test_hardware():
    """Test Hardware Monitor."""
    print("\n🖥️  Testing Hardware Monitor...")
    hw = MonsterDogHardwareMonitor()
    
    report = hw.full_report()
    
    print(f"  ✓ System: {report['system']['system']} {report['system']['release']}")
    print(f"  ✓ CPU: {report['cpu']['physical_cores']} cores, {report['cpu']['usage_percent']}% used")
    print(f"  ✓ RAM: {report['memory']['percent']}% used ({report['memory']['used'] / (1024**3):.1f} GB / {report['memory']['total'] / (1024**3):.1f} GB)")
    print(f"  ✓ Disk: {report['disk']['percent']}% used")
    return True


def test_quantum_core():
    """Test Quantum Core."""
    print("\n⚛️  Testing Quantum Core...")
    core = MonsterDogQuantumCore()
    
    # Test initial state
    print(f"  ✓ Initial coherence: {core.coherence}")
    print(f"  ✓ Initial entropy: {core.entropy}")
    
    # Run simulation steps
    print("  ⚙️  Running 10 simulation cycles...")
    for i in range(10):
        state = core.step()
    
    print(f"  ✓ Final coherence: {state['coherence']}")
    print(f"  ✓ Final entropy: {state['entropy']}")
    print(f"  ✓ Stability: {state['stability']}")
    print(f"  ✓ Frequency: {state['frequency']} Hz")
    return True


async def test_agents():
    """Test Agentic System."""
    print("\n🤖 Testing Agentic System...")
    system = AgenticSystem()
    
    print(f"  ✓ Agents loaded: {len(system.agents)}")
    for agent in system.agents:
        print(f"    - {agent.name} ({agent.mode.value})")
    
    # Execute agents
    result = await system.execute_all()
    print(f"  ✓ Agents executed: {result['active_count']} active")
    
    # Test auto-pivot
    print("  ⚙️  Testing Auto-Pivot...")
    system.auto_pivot(coherence=0.8, entropy=0.2)
    print(f"  ✓ Mode after high coherence: {system.system_mode.value}")
    
    system.auto_pivot(coherence=0.2, entropy=0.8)
    print(f"  ✓ Mode after high entropy: {system.system_mode.value}")
    
    return True


def test_orchestrator():
    """Test Supreme Orchestrator (FastAPI app)."""
    print("\n🎛️  Testing Supreme Orchestrator...")
    
    print(f"  ✓ App title: {app.title}")
    print(f"  ✓ App version: {app.version}")
    print(f"  ✓ Available endpoints:")
    
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            methods = ', '.join(route.methods) if route.methods else 'WS'
            print(f"    - {route.path} [{methods}]")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("MONSTERDOG FRAMEWORK vΩ - SYSTEM VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("AEGIS Security", test_security),
        ("Hardware Monitor", test_hardware),
        ("Quantum Core", test_quantum_core),
        ("Supreme Orchestrator", test_orchestrator),
    ]
    
    # Synchronous tests
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results[name] = False
    
    # Async tests
    try:
        print("\n🔄 Running async tests...")
        asyncio.run(test_agents())
        results["Agentic System"] = True
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        results["Agentic System"] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:.<40} {status}")
    
    print("=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS OPERATIONAL - MONSTERDOG vΩ READY!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
