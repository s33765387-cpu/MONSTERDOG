#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour MONSTERDOG FRAMEWORK vΩ
"""

import unittest
import asyncio
from monsterdog.core import MonsterDogQuantumCore
from monsterdog.agents import AgenticSystem, PivotMode
from monsterdog.security import AegisSecurity
from monsterdog.hardware import MonsterDogHardwareMonitor


class TestQuantumCore(unittest.TestCase):
    """Tests pour le Quantum Core."""
    
    def test_initialization(self):
        """Test l'initialisation du noyau quantique."""
        core = MonsterDogQuantumCore()
        self.assertEqual(core.cycle_count, 0)
        self.assertAlmostEqual(core.coherence, 0.5)
        self.assertAlmostEqual(core.entropy, 0.5)
        
    def test_step(self):
        """Test une itération du noyau."""
        core = MonsterDogQuantumCore()
        state = core.step()
        
        self.assertEqual(state["cycle"], 1)
        self.assertIn("coherence", state)
        self.assertIn("entropy", state)
        self.assertIn("stability", state)
        self.assertEqual(state["frequency"], 11.987)
        
    def test_multiple_steps(self):
        """Test plusieurs itérations."""
        core = MonsterDogQuantumCore()
        for i in range(10):
            state = core.step()
            self.assertEqual(state["cycle"], i + 1)
            
    def test_reset(self):
        """Test la réinitialisation."""
        core = MonsterDogQuantumCore()
        core.step()
        core.step()
        core.reset()
        self.assertEqual(core.cycle_count, 0)


class TestAgenticSystem(unittest.TestCase):
    """Tests pour le système agentique."""
    
    def test_initialization(self):
        """Test l'initialisation du système."""
        system = AgenticSystem()
        self.assertEqual(len(system.agents), 3)
        self.assertEqual(system.system_mode, PivotMode.MODE_A)
        
    def test_execute_all(self):
        """Test l'exécution de tous les agents."""
        system = AgenticSystem()
        
        async def run_test():
            result = await system.execute_all()
            self.assertIn("agents", result)
            self.assertIn("system_mode", result)
            self.assertEqual(len(result["agents"]), 3)
            
        asyncio.run(run_test())
        
    def test_auto_pivot(self):
        """Test l'auto-pivot basé sur la cohérence/entropie."""
        system = AgenticSystem()
        
        # Test Mode A (haute entropie)
        system.auto_pivot(coherence=0.3, entropy=0.8)
        self.assertEqual(system.system_mode, PivotMode.MODE_A)
        
        # Test Mode B (haute cohérence)
        system.auto_pivot(coherence=0.8, entropy=0.3)
        self.assertEqual(system.system_mode, PivotMode.MODE_B)
        
        # Test Mode C (équilibre)
        system.auto_pivot(coherence=0.5, entropy=0.5)
        self.assertEqual(system.system_mode, PivotMode.MODE_C)


class TestAegisSecurity(unittest.TestCase):
    """Tests pour le module de sécurité AEGIS."""
    
    def test_token_generation(self):
        """Test la génération de tokens."""
        aegis = AegisSecurity()
        token = aegis.generate_token()
        
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 128)  # SHA-512 = 128 hex chars
        
    def test_token_verification(self):
        """Test la vérification de tokens."""
        aegis = AegisSecurity()
        token = aegis.generate_token()
        
        self.assertTrue(aegis.verify(token))
        self.assertFalse(aegis.verify("invalid_token"))
        
    def test_unique_tokens(self):
        """Test l'unicité des tokens."""
        aegis = AegisSecurity()
        token1 = aegis.generate_token()
        token2 = aegis.generate_token()
        
        self.assertNotEqual(token1, token2)


class TestHardwareMonitor(unittest.TestCase):
    """Tests pour le moniteur matériel."""
    
    def test_cpu_info(self):
        """Test les informations CPU."""
        hw = MonsterDogHardwareMonitor()
        cpu = hw.get_cpu_info()
        
        self.assertIn("physical_cores", cpu)
        self.assertIn("logical_cores", cpu)
        self.assertIn("usage_percent", cpu)
        self.assertGreater(cpu["physical_cores"], 0)
        
    def test_memory_info(self):
        """Test les informations mémoire."""
        hw = MonsterDogHardwareMonitor()
        mem = hw.get_memory_info()
        
        self.assertIn("total", mem)
        self.assertIn("available", mem)
        self.assertIn("percent", mem)
        self.assertGreater(mem["total"], 0)
        
    def test_full_report(self):
        """Test le rapport complet."""
        hw = MonsterDogHardwareMonitor()
        report = hw.full_report()
        
        self.assertIn("system", report)
        self.assertIn("cpu", report)
        self.assertIn("memory", report)
        self.assertIn("disk", report)
        self.assertIn("network", report)


if __name__ == "__main__":
    unittest.main()
