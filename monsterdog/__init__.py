"""
MONSTERDOG FRAMEWORK vΩ
Architecture IA Quantique & Agentique
Fréquence: 11.987 Hz
"""

__version__ = "11.987.0"
__author__ = "Samuel Cloutier (ZORG-MASTER)"

from .core import MonsterDogQuantumCore
from .agents import AgenticSystem
from .hardware import MonsterDogHardwareMonitor
from .security import AegisSecurity

__all__ = [
    "MonsterDogQuantumCore",
    "AgenticSystem",
    "MonsterDogHardwareMonitor",
    "AegisSecurity",
]
