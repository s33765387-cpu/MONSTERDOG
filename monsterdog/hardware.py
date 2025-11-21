#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONSTERDOG HARDWARE MONITOR - Partie V
Système de surveillance matérielle
"""

import psutil
from typing import Dict, Any


class MonsterDogHardwareMonitor:
    """
    Moniteur matériel pour surveiller les ressources système.
    Fournit des informations sur CPU, RAM, disque, et réseau.
    """
    
    def __init__(self):
        self.boot_time = psutil.boot_time()
        
    def get_cpu_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le CPU."""
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "usage_percent": psutil.cpu_percent(interval=0.1),
            "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Retourne les informations sur la mémoire."""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }
    
    def get_disk_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le disque."""
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    
    def get_network_info(self) -> Dict[str, Any]:
        """Retourne les informations réseau."""
        net = psutil.net_io_counters()
        return {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Retourne les informations système générales."""
        import platform
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    
    def full_report(self) -> Dict[str, Any]:
        """Génère un rapport complet du système."""
        return {
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info()
        }
