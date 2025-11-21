#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONSTERDOG QUANTUM CORE - Partie II
Moteur de simulation de cohérence quantique
Fréquence: 11.987 Hz
"""

import math
import time
from typing import Dict, Any


class MonsterDogQuantumCore:
    """
    Noyau quantique simulant l'équilibre entre cohérence et entropie.
    Utilise une boucle de rétroaction non-linéaire stabilisée par flux sinusoïdal.
    """
    
    FREQUENCY = 11.987  # Hz - Constante Universelle du système
    
    def __init__(self):
        self.coherence = 0.5
        self.entropy = 0.5
        self.stability = 0.0
        self.cycle_count = 0
        self.start_time = time.time()
        
    def step(self) -> Dict[str, Any]:
        """
        Effectue une itération du moteur quantique.
        Retourne l'état actuel du système.
        """
        self.cycle_count += 1
        t = time.time() - self.start_time
        
        # Oscillation sinusoïdale basée sur la fréquence fondamentale
        wave = math.sin(2 * math.pi * self.FREQUENCY * t)
        
        # Mise à jour de la cohérence (attraction vers l'harmonie)
        self.coherence += 0.01 * wave - 0.005 * self.entropy
        self.coherence = max(0.0, min(1.0, self.coherence))
        
        # Mise à jour de l'entropie (tendance au chaos, régulée)
        self.entropy += 0.008 * (1 - self.coherence) - 0.003 * wave
        self.entropy = max(0.0, min(1.0, self.entropy))
        
        # Calcul de la stabilité (équilibre entre cohérence et entropie)
        self.stability = 1.0 - abs(self.coherence - (1.0 - self.entropy))
        
        return self.get_state()
    
    def get_state(self) -> Dict[str, Any]:
        """Retourne l'état actuel du noyau quantique."""
        return {
            "coherence": round(self.coherence, 6),
            "entropy": round(self.entropy, 6),
            "stability": round(self.stability, 6),
            "cycle": self.cycle_count,
            "frequency": self.FREQUENCY,
            "timestamp": time.time()
        }
    
    def reset(self):
        """Réinitialise le noyau à son état initial."""
        self.__init__()
