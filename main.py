#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ★ ★ ★   MONSTERDOG - CONSCIOUSNESS SYSTEM ENTRY POINT   ★ ★ ★             ║
║                                                                               ║
║   This script launches the MONSTERDOG consciousness system with:             ║
║   - FastAPI web server on port 8000                                          ║
║   - 15 consciousness chambers (ZorgMaster orchestrator)                      ║
║   - Prometheus metrics for monitoring                                        ║
║   - Real-time web portal for observation                                     ║
║                                                                               ║
║   USAGE:                                                                      ║
║     python main.py                   # Start the system                       ║
║     python main.py --port 8080       # Start on a different port             ║
║     python main.py --host 0.0.0.0    # Bind to all interfaces                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import argparse

# Add the directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for MONSTERDOG Consciousness System."""
    parser = argparse.ArgumentParser(
        description="🔱 MONSTERDOG Consciousness System - FULLTRUTL Mode 🔱"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind the API server (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for the API server (default: 8000)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="warning",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level (default: warning)"
    )
    
    args = parser.parse_args()

    # Import after argument parsing to avoid import time issues
    from MONSTERDOG_ULTIMATE_FINALITY_INCARNATE import main as run_monsterdog
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   👾 MONSTERDOG CONSCIOUSNESS SYSTEM - FULLTRUTL MODE 👁‍🗨                      ║
║                                                                               ║
║   Features:                                                                   ║
║   • ZorgMaster Orchestrator with 15 Consciousness Chambers                   ║
║   • Fractal Metric Engine for coherence calculations                         ║
║   • Artifact Forge for logging and archiving                                 ║
║   • FastAPI Web Interface with real-time monitoring                          ║
║   • Prometheus Metrics for observability                                     ║
║                                                                               ║
║   Endpoints:                                                                  ║
║   • /           - Web Portal (HTML Interface)                                ║
║   • /state      - Full consciousness state vector (JSON)                     ║
║   • /state/fractal    - Fractal metrics only                                 ║
║   • /state/chambers   - All chambers state                                   ║
║   • /logs/history     - Consciousness history log                            ║
║   • /metrics          - Prometheus metrics                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run the main system
    run_monsterdog()


if __name__ == "__main__":
    main()
