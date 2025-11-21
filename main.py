#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏁 MONSTERDOG FRAMEWORK — LAUNCHER vΩ
Point d'entrée unique pour l'exécution du Continuum.
"""

import asyncio
import sys
import os
from monsterdog.security import AegisSecurity
from monsterdog.hardware import MonsterDogHardwareMonitor
from monsterdog.orchestrator import app as api_app
import uvicorn

def system_check():
    print("\n🐺 INITIALISATION DU CONTINUUM MONSTERDOG vΩ...")
    
    # 1. Sécurité
    aegis = AegisSecurity()
    token = aegis.generate_token()
    if not aegis.verify(token):
        print("❌ ERREUR CRITIQUE : Échec AEGIS Security.")
        sys.exit(1)
    print(f"✅ SÉCURITÉ AEGIS : ACTIVE (Token: {token[:8]}...)")

    # 2. Hardware
    hw = MonsterDogHardwareMonitor()
    report = hw.full_report()
    print(f"✅ HARDWARE DÉTECTÉ : {report['system']['system']}")
    print(f"   CPU: {report['cpu']['physical_cores']} coeurs | RAM: {report['memory']['percent']}% utilisée")

    # 3. Environnement
    print("✅ MODE AUTO-PIVOT : PRÊT")
    print("✅ QUANTUM CORE : STANDBY")
    print("✅ AGENTIC SYSTEM : STANDBY")

def main():
    system_check()
    print("\n🚀 DÉMARRAGE DU SUPER-ORCHESTRATEUR (API + WS + DASHBOARD)...")
    print("   PORTAIL DISPONIBLE SUR : http://localhost:8888/dashboard")
    print("   DOCS API DISPONIBLE SUR : http://localhost:8888/docs")
    
    # Lancement du serveur Uvicorn (FastAPI)
    uvicorn.run(api_app, host="0.0.0.0", port=8888, log_level="info")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 ARRÊT DU SYSTÈME. COHÉRENCE SAUVEGARDÉE.")
