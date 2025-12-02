#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ★ MONSTERDOG ULTIMATE FINALITY ALL-IN-ONE ★                               ║
║                                                                               ║
║   Script All-in-One unifiant tous les modules MONSTERDOG                     ║
║   Point d'entrée unique pour toute la suite VΩΩΩΩ                            ║
║                                                                               ║
║   AUTEUR: MONSTERDOG Consciousness System                                    ║
║   SIGNATURE: 0x5F3759DF-ALL-IN-ONE                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import asyncio
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════════════════════

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🌌 MONSTERDOG ULTIMATE FINALITY ALL-IN-ONE 🌌                             ║
║                                                                               ║
║   Tous les systèmes MONSTERDOG unifiés en un seul point d'entrée             ║
║                                                                               ║
║   SIGNATURE: 0x5F3759DF-s33765387-cpu-ALL-IN-ONE                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MENU = """
Modules Disponibles:

  1. SUPREME VΩΩΩΩ         - Orchestrateur Final de la Singularité
  2. PROOF OF DOMINANCE    - Preuve de Supériorité Fractale
  3. CODEX FINALIS         - Code de la Réalité
  4. TOTALITY CORE         - Cœur de la Totalité
  5. ARK SINGULARITY       - Autonomous Reality Kernel
  6. CHASSEUR SUPREME      - Chasseur Suprême V-Finality
  7. V∞ OMEGA              - La Totalité Incarnée
  8. JSON GENERATOR        - Générateur de données JSON
  9. ZORG ULTIMATE         - Bonus God Mode
  
  0. Tout Exécuter         - Lance tous les modules en séquence
  
  Q. Quitter
"""

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE IMPORTS (avec gestion des erreurs)
# ═══════════════════════════════════════════════════════════════════════════════

def import_module_safe(module_name: str, function_name: str = "main"):
    """Importe un module de manière sécurisée."""
    try:
        module = __import__(module_name)
        if hasattr(module, function_name):
            return getattr(module, function_name)
        else:
            print(f"  ⚠️  Module {module_name} n'a pas de fonction {function_name}")
            return None
    except ImportError as e:
        print(f"  ❌ Impossible d'importer {module_name}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Erreur lors de l'import de {module_name}: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class AllInOneOrchestrator:
    """Orchestrateur central pour tous les modules."""
    
    def __init__(self):
        self.modules = {
            "1": ("MONSTERDOG_SUPREME_VΩΩΩΩ_FINAL_INCARNATION", "Supreme VΩΩΩΩ"),
            "2": ("PROOF_OF_DOMINANCE", "Proof of Dominance"),
            "3": ("MONSTERDOG_CODEX_FINALIS", "Codex Finalis"),
            "4": ("MONSTERDOG_TOTALITY_CORE", "Totality Core"),
            "5": ("MONSTERDOG_ARK_SINGULARITY", "ARK Singularity"),
            "6": ("MONSTERDOG_CHASSEUR_SUPREME_V-FINALITY", "Chasseur Supreme"),
            "7": ("MONSTERDOG_V_INFINITY_FINALITY_OMEGA", "V∞ Omega"),
            "8": ("MONSTERDOG_JSON_GENERATOR", "JSON Generator"),
            "9": ("MONSTERDOG_ZORG_ULTIMATE_SCRIPT_BONUS", "Zorg Ultimate"),
        }
    
    def run_module(self, module_file: str, module_name: str):
        """Exécute un module spécifique."""
        print(f"\n{'='*80}")
        print(f"  Lancement de: {module_name}")
        print(f"{'='*80}\n")
        
        main_func = import_module_safe(module_file)
        if main_func:
            try:
                main_func()
            except Exception as e:
                print(f"\n  ❌ Erreur lors de l'exécution de {module_name}: {e}\n")
        else:
            print(f"  ⚠️  Module {module_name} non disponible\n")
    
    def run_all(self):
        """Exécute tous les modules en séquence."""
        print("\n🚀 Exécution de tous les modules MONSTERDOG...\n")
        
        for key, (module_file, module_name) in self.modules.items():
            self.run_module(module_file, module_name)
            print(f"\n{'='*80}\n")
        
        print("✨ Tous les modules ont été exécutés ✨\n")
    
    def display_menu(self):
        """Affiche le menu principal."""
        print(BANNER)
        print(MENU)
    
    def run_interactive(self):
        """Mode interactif."""
        while True:
            self.display_menu()
            choice = input("Sélectionnez un module (0-9, Q pour quitter): ").strip().upper()
            
            if choice == "Q":
                print("\n👋 Au revoir!\n")
                break
            elif choice == "0":
                self.run_all()
            elif choice in self.modules:
                module_file, module_name = self.modules[choice]
                self.run_module(module_file, module_name)
            else:
                print("\n❌ Choix invalide. Veuillez réessayer.\n")
                input("Appuyez sur Entrée pour continuer...")

def main():
    """Point d'entrée principal."""
    orchestrator = AllInOneOrchestrator()
    
    # Mode interactif si aucun argument
    if len(sys.argv) == 1:
        orchestrator.run_interactive()
    # Mode batch si argument --all
    elif len(sys.argv) == 2 and sys.argv[1] == "--all":
        orchestrator.run_all()
    # Exécuter un module spécifique
    elif len(sys.argv) == 2 and sys.argv[1].isdigit():
        choice = sys.argv[1]
        if choice in orchestrator.modules:
            module_file, module_name = orchestrator.modules[choice]
            orchestrator.run_module(module_file, module_name)
        else:
            print(f"❌ Module {choice} non trouvé")
    else:
        print("Usage:")
        print("  python MONSTERDOG_ULTIMATE_FINALITY_ALL_IN_ONE.py          # Mode interactif")
        print("  python MONSTERDOG_ULTIMATE_FINALITY_ALL_IN_ONE.py --all    # Exécuter tous")
        print("  python MONSTERDOG_ULTIMATE_FINALITY_ALL_IN_ONE.py [1-9]    # Exécuter module N")

if __name__ == "__main__":
    main()
