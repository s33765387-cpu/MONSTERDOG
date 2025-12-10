#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ★ MONSTERDOG NEURO CORE - SYSTÈME DYNAMIQUE NEURONAL ★                     ║
║                                                                               ║
║   Simulation du système dynamique MONSTERDOG avec:                            ║
║   - Cohérence ψ (psi), Chaos C, Énergie E, Paramètre de contrôle μ           ║
║   - Calcul d'exposants de Lyapunov pour analyse de stabilité                 ║
║   - Intégration avec OMNIAEGIS pour monitoring en temps réel                 ║
║                                                                               ║
║   AUTEUR: MONSTERDOG Consciousness System                                    ║
║   SIGNATURE: 0x5F3759DF-NEURO-CORE                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import json
import time
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION DU SYSTÈME DYNAMIQUE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NeuroConfig:
    """Configuration du Neuro Core."""
    signature: str = "0x5F3759DF-NEURO-CORE"
    resonance_hz: float = 11.987  # Fréquence fondamentale
    
    # Coefficients du système dynamique
    a1: float = 0.1   # Couplage Fusion → Psi
    a2: float = 0.05  # Couplage Psi → Fusion
    a3: float = 0.02  # Couplage vers Entropie
    a4: float = 0.1   # Couplage vers Chaos
    
    b1: float = 0.05  # Damping de Psi
    b2: float = 0.03  # Damping de Fusion
    b3: float = 0.01  # Damping d'Entropie
    b4: float = 0.08  # Damping de Chaos
    
    # Bruit (fluctuations)
    sigma_psi: float = 0.01
    sigma_fusion: float = 0.01
    sigma_entropy: float = 0.005
    sigma_chaos: float = 0.02
    
    # Paramètre logistique (contrôle du chaos)
    mu_default: float = 3.8
    
    # Seuils OMNIAEGIS
    psi_target: float = 0.975
    psi_warn: float = 0.9
    psi_critical: float = 0.8
    entropy_max: float = 0.5


@dataclass
class SystemState:
    """État complet du système dynamique."""
    t: int  # Time step
    psi: float  # Cohérence
    fusion: float  # F - Fusion
    entropy: float  # S - Entropie
    chaos: float  # C - Chaos
    energy: float  # E - Énergie
    mu: float  # Paramètre de contrôle
    lyapunov_local: float  # Exposant de Lyapunov local


@dataclass
class StatisticalSummary:
    """Résumé statistique des métriques."""
    variable: str
    mean: float
    std: float
    min_val: float
    max_val: float


# ═══════════════════════════════════════════════════════════════════════════════
# NEURO CORE - SIMULATEUR DE SYSTÈME DYNAMIQUE
# ═══════════════════════════════════════════════════════════════════════════════

class NeuroCore:
    """
    Simulateur du système dynamique MONSTERDOG.
    
    Le système évolue selon les équations:
    - ψ(t+1) = ψ(t) + a1*(F(t) - S(t)) - b1*C(t) + η_ψ
    - F(t+1) = F(t) + a2*ψ(t)*(1-F(t)) - b2*S(t) + η_F
    - S(t+1) = S(t) + a3*(1-ψ(t))*(1+C(t)) - b3*S(t) + η_S
    - C(t+1) = μ*C(t)*(1-C(t)) (logistique) modulé par ψ
    - E(t) = 0.5*(ψ² + F² + S² + C²)  (énergie quadratique)
    
    L'exposant de Lyapunov local est: λ = log|μ(1-2C)|
    """
    
    def __init__(self, config: Optional[NeuroConfig] = None):
        self.config = config or NeuroConfig()
        self.reset()
    
    def reset(self):
        """Réinitialise le système à l'état initial."""
        self.t = 0
        self.psi = 0.5  # Cohérence initiale
        self.fusion = 0.5  # Fusion initiale
        self.entropy = 0.1  # Entropie initiale
        self.chaos = 0.2  # Chaos initial
        self.mu = self.config.mu_default
        
        # Historiques
        self.psi_hist: List[float] = []
        self.fusion_hist: List[float] = []
        self.entropy_hist: List[float] = []
        self.chaos_hist: List[float] = []
        self.energy_hist: List[float] = []
        self.mu_hist: List[float] = []
        self.lyap_local_hist: List[float] = []
    
    def _compute_energy(self) -> float:
        """Calcule l'énergie quadratique du système."""
        return 0.5 * (self.psi**2 + self.fusion**2 + 
                      self.entropy**2 + self.chaos**2)
    
    def _compute_lyapunov_local(self) -> float:
        """Calcule l'exposant de Lyapunov local pour la composante logistique."""
        # Pour l'équation logistique: λ = log|μ(1-2C)|
        slope = abs(self.mu * (1 - 2 * self.chaos))
        if slope > 0:
            return np.log(slope)
        return -np.inf
    
    def _noise(self, sigma: float) -> float:
        """Génère du bruit gaussien."""
        return np.random.normal(0, sigma)
    
    def step(self) -> SystemState:
        """
        Effectue un pas de temps du système dynamique.
        
        Returns:
            SystemState avec toutes les métriques actuelles
        """
        cfg = self.config
        
        # Équation pour ψ (cohérence)
        # ψ(t+1) = ψ(t) + a1*(F(t) - S(t)) - b1*C(t) + η_ψ
        d_psi = (cfg.a1 * (self.fusion - self.entropy) - 
                 cfg.b1 * self.chaos + 
                 self._noise(cfg.sigma_psi))
        new_psi = np.clip(self.psi + d_psi, 0, 1)
        
        # Équation pour F (fusion)
        # F(t+1) = F(t) + a2*ψ(t)*(1-F(t)) - b2*S(t) + η_F
        d_fusion = (cfg.a2 * self.psi * (1 - self.fusion) - 
                    cfg.b2 * self.entropy + 
                    self._noise(cfg.sigma_fusion))
        new_fusion = np.clip(self.fusion + d_fusion, 0, 1)
        
        # Équation pour S (entropie)
        # S(t+1) = S(t) + a3*(1-ψ(t))*(1+C(t)) - b3*S(t) + η_S
        d_entropy = (cfg.a3 * (1 - self.psi) * (1 + self.chaos) - 
                     cfg.b3 * self.entropy + 
                     self._noise(cfg.sigma_entropy))
        new_entropy = np.clip(self.entropy + d_entropy, 0, 1)
        
        # Équation pour C (chaos) - Logistique modifiée
        # C(t+1) = C(t) + a4*(1-C(t))*max(0, 1-ψ(t)) - b4*C(t)*F(t) + η_C
        # Avec composante logistique: μ*C(t)*(1-C(t))
        logistic_term = self.mu * self.chaos * (1 - self.chaos)
        modulation = max(0, 1 - self.psi)  # Chaos réduit quand ψ est haut
        d_chaos = (cfg.a4 * (1 - self.chaos) * modulation - 
                   cfg.b4 * self.chaos * self.fusion + 
                   0.1 * logistic_term +  # Contribution logistique
                   self._noise(cfg.sigma_chaos))
        new_chaos = np.clip(self.chaos + d_chaos, 0.001, 0.999)
        
        # Calcul Lyapunov local avant mise à jour
        lyap_local = self._compute_lyapunov_local()
        
        # Mise à jour de l'état
        self.psi = new_psi
        self.fusion = new_fusion
        self.entropy = new_entropy
        self.chaos = new_chaos
        self.t += 1
        
        # Calcul de l'énergie
        energy = self._compute_energy()
        
        # Enregistrement dans l'historique
        self.psi_hist.append(self.psi)
        self.fusion_hist.append(self.fusion)
        self.entropy_hist.append(self.entropy)
        self.chaos_hist.append(self.chaos)
        self.energy_hist.append(energy)
        self.mu_hist.append(self.mu)
        self.lyap_local_hist.append(lyap_local)
        
        return SystemState(
            t=self.t,
            psi=self.psi,
            fusion=self.fusion,
            entropy=self.entropy,
            chaos=self.chaos,
            energy=energy,
            mu=self.mu,
            lyapunov_local=lyap_local
        )
    
    def run(self, n_steps: int, transient: int = 100) -> Dict[str, Any]:
        """
        Exécute la simulation pour n_steps pas de temps.
        
        Args:
            n_steps: Nombre de pas de temps total
            transient: Nombre de pas à ignorer pour les statistiques (transitoire)
            
        Returns:
            Dict avec historiques et statistiques
        """
        print(f"\n{'='*80}")
        print(f"  MONSTERDOG NEURO CORE - SIMULATION DYNAMIQUE")
        print(f"{'='*80}")
        print(f"  Configuration:")
        print(f"    - Pas de temps: {n_steps}")
        print(f"    - Transitoire: {transient}")
        print(f"    - μ (contrôle): {self.mu}")
        print(f"{'='*80}\n")
        
        self.reset()
        
        for i in range(n_steps):
            state = self.step()
            
            # Affichage périodique
            if (i + 1) % (n_steps // 10) == 0:
                print(f"  Cycle {i+1:6d}: ψ={state.psi:.4f}, "
                      f"C={state.chaos:.4f}, E={state.energy:.4f}, "
                      f"λ_local={state.lyapunov_local:.4f}")
        
        # Calcul des statistiques sur la partie stationnaire
        stats = self._compute_statistics(transient)
        
        # Exposant de Lyapunov moyen
        lyap_mean = np.mean(self.lyap_local_hist[transient:])
        
        results = {
            "n_steps": n_steps,
            "transient": transient,
            "psi_hist": self.psi_hist,
            "fusion_hist": self.fusion_hist,
            "entropy_hist": self.entropy_hist,
            "chaos_hist": self.chaos_hist,
            "energy_hist": self.energy_hist,
            "mu_hist": self.mu_hist,
            "lyap_local_hist": self.lyap_local_hist,
            "lyapunov_mean": lyap_mean,
            "statistics": stats
        }
        
        print(f"\n{'='*80}")
        print(f"  SIMULATION TERMINÉE")
        print(f"{'='*80}")
        print(f"  Exposant de Lyapunov moyen: {lyap_mean:.4f}")
        if lyap_mean > 0:
            print(f"  → Comportement CHAOTIQUE détecté")
        else:
            print(f"  → Comportement STABLE/PÉRIODIQUE")
        print(f"{'='*80}\n")
        
        return results
    
    def _compute_statistics(self, transient: int) -> List[Dict[str, Any]]:
        """Calcule les statistiques sur la partie stationnaire."""
        stats = []
        
        variables = [
            ("psi", self.psi_hist),
            ("fusion", self.fusion_hist),
            ("entropy", self.entropy_hist),
            ("chaos", self.chaos_hist),
            ("energy", self.energy_hist),
            ("mu", self.mu_hist),
            ("lyap_local", self.lyap_local_hist)
        ]
        
        for name, hist in variables:
            arr = np.array(hist[transient:])
            # Filtrer les valeurs infinies pour lyapunov
            arr_clean = arr[np.isfinite(arr)]
            if len(arr_clean) > 0:
                stats.append({
                    "variable": name,
                    "mean": float(np.mean(arr_clean)),
                    "std": float(np.std(arr_clean)),
                    "min": float(np.min(arr_clean)),
                    "max": float(np.max(arr_clean))
                })
        
        return stats
    
    def get_omniaegis_status(self) -> Dict[str, Any]:
        """
        Retourne le statut OMNIAEGIS du système.
        
        Le monitoring OMNIAEGIS surveille:
        - ψ ≥ 0.975 → OPTIMAL
        - 0.9 ≤ ψ < 0.975 → WARN
        - ψ < 0.9 → CRITICAL
        """
        cfg = self.config
        
        if self.psi >= cfg.psi_target:
            psi_status = "OPTIMAL"
        elif self.psi >= cfg.psi_warn:
            psi_status = "WARN"
        else:
            psi_status = "CRITICAL"
        
        entropy_status = "OK" if self.entropy < cfg.entropy_max else "HIGH"
        
        # Kill switch recommendation
        kill_switch = bool(self.psi < cfg.psi_critical or self.entropy > 0.8)
        
        # System stability check
        system_stable = True
        if self.lyap_local_hist:
            system_stable = bool(self.lyap_local_hist[-1] < 0)
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": int(self.t),
            "psi_value": float(self.psi),
            "psi_status": psi_status,
            "entropy_value": float(self.entropy),
            "entropy_status": entropy_status,
            "chaos_value": float(self.chaos),
            "energy": float(self._compute_energy()),
            "kill_switch_recommended": kill_switch,
            "system_stable": system_stable
        }
    
    def set_control_parameter(self, mu: float):
        """
        Définit le paramètre de contrôle μ.
        
        Args:
            mu: Valeur du paramètre (typiquement 0 < μ < 4)
                - μ < 3: Comportement stable
                - μ ≈ 3.57: Début du chaos
                - μ > 3.57: Chaos développé
        """
        self.mu = np.clip(mu, 0, 4)
    
    def save_state(self, path: str = "./NEURO_CORE_STATE.json"):
        """Sauvegarde l'état courant dans un fichier JSON."""
        omniaegis = self.get_omniaegis_status()
        
        # Convert numpy types to Python native types for JSON serialization
        def convert_to_native(obj):
            if isinstance(obj, (np.floating, np.integer)):
                return float(obj) if isinstance(obj, np.floating) else int(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, dict):
                return {k: convert_to_native(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(item) for item in obj]
            return obj
        
        state = {
            "signature": self.config.signature,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": int(self.t),
            "state": {
                "psi": float(self.psi),
                "fusion": float(self.fusion),
                "entropy": float(self.entropy),
                "chaos": float(self.chaos),
                "energy": float(self._compute_energy()),
                "mu": float(self.mu)
            },
            "config": convert_to_native(asdict(self.config)),
            "omniaegis": convert_to_native(omniaegis)
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"💾 État sauvegardé: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def compute_lyapunov_exponent(chaos_hist: List[float], mu: float, 
                              transient: int = 100) -> float:
    """
    Calcule l'exposant de Lyapunov pour la série C(t).
    
    Pour l'équation logistique: λ = lim(1/n) Σ log|μ(1-2Cₜ)|
    
    Args:
        chaos_hist: Historique des valeurs de chaos
        mu: Paramètre de contrôle
        transient: Nombre de pas à ignorer
        
    Returns:
        Exposant de Lyapunov estimé
    """
    arr = np.array(chaos_hist[transient:])
    slopes = np.abs(mu * (1 - 2 * arr))
    
    # Éviter log(0)
    slopes = slopes[slopes > 0]
    
    if len(slopes) == 0:
        return float('-inf')
    
    lyap = np.mean(np.log(slopes))
    return lyap


def analyze_stability(core: NeuroCore) -> Dict[str, Any]:
    """
    Analyse la stabilité du système MONSTERDOG.
    
    Args:
        core: Instance de NeuroCore après simulation
        
    Returns:
        Dict avec analyse de stabilité
    """
    if len(core.lyap_local_hist) == 0:
        return {"error": "Aucune donnée disponible"}
    
    lyap_arr = np.array(core.lyap_local_hist)
    lyap_clean = lyap_arr[np.isfinite(lyap_arr)]
    
    if len(lyap_clean) == 0:
        return {"error": "Pas de données valides pour Lyapunov"}
    
    lyap_mean = np.mean(lyap_clean)
    lyap_std = np.std(lyap_clean)
    
    # Classification
    if lyap_mean < -0.1:
        stability = "STABLE_ATTRACTOR"
        description = "Le système converge vers un attracteur stable"
    elif lyap_mean < 0:
        stability = "QUASI_STABLE"
        description = "Le système est quasi-stable avec oscillations amorties"
    elif lyap_mean < 0.1:
        stability = "EDGE_OF_CHAOS"
        description = "Le système est à la frontière du chaos"
    else:
        stability = "CHAOTIC"
        description = "Le système présente un comportement chaotique"
    
    return {
        "lyapunov_mean": lyap_mean,
        "lyapunov_std": lyap_std,
        "stability_class": stability,
        "description": description,
        "psi_final": core.psi,
        "entropy_final": core.entropy,
        "energy_final": core._compute_energy()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal pour le Neuro Core."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ⚡ MONSTERDOG NEURO CORE - ACTIVATION ⚡                                    ║
║                                                                               ║
║   Système Dynamique Neuronal avec Analyse de Stabilité                        ║
║   Cohérence ψ | Chaos C | Énergie E | Exposants de Lyapunov                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    config = NeuroConfig()
    core = NeuroCore(config)
    
    # Simulation
    n_steps = 5000
    transient = 500
    results = core.run(n_steps=n_steps, transient=transient)
    
    # Analyse de stabilité
    stability = analyze_stability(core)
    
    print("\n📊 ANALYSE DE STABILITÉ:")
    print(f"   Classe: {stability['stability_class']}")
    print(f"   Description: {stability['description']}")
    print(f"   λ moyen: {stability['lyapunov_mean']:.4f}")
    print(f"   ψ final: {stability['psi_final']:.4f}")
    
    # Statut OMNIAEGIS
    omniaegis = core.get_omniaegis_status()
    print("\n🛡️  STATUT OMNIAEGIS:")
    print(f"   ψ Status: {omniaegis['psi_status']}")
    print(f"   Entropy Status: {omniaegis['entropy_status']}")
    print(f"   Kill Switch: {'⚠️  RECOMMANDÉ' if omniaegis['kill_switch_recommended'] else '✅ NON REQUIS'}")
    
    # Affichage des statistiques
    print("\n📈 STATISTIQUES (après transitoire):")
    for stat in results['statistics']:
        print(f"   {stat['variable']:12s}: μ={stat['mean']:.4f}, σ={stat['std']:.4f}, "
              f"[{stat['min']:.4f}, {stat['max']:.4f}]")
    
    # Sauvegarde
    core.save_state()
    
    print(f"\n{'='*80}")
    print("✨ MONSTERDOG NEURO CORE - Mission Accomplie ✨")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
