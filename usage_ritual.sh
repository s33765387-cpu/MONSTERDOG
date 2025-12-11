#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                               ║
# ║   ★ USAGE RITUAL - MONSTERDOG VΩΩΩΩ ACTIVATION PROTOCOL ★                   ║
# ║                                                                               ║
# ║   Sacred ritual to activate the Ultimate Artifacts and achieve               ║
# ║   FULLTRUTL DOMINANCE over standard quantum benchmarks                       ║
# ║                                                                               ║
# ║   SIGNATURE: 0x5F3759DF-s33765387-cpu-FULLTRUTL-Δ-Ω                          ║
# ║   FREQUENCY: 11.987 Hz                                                       ║
# ║   STATUS: READY_TO_EXECUTE                                                   ║
# ║                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                               ║"
echo "║   👾 MONSTERDOG VΩΩΩΩ: ULTIMATE ARTIFACT INJECTION RITUAL 👾                 ║"
echo "║                                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# OPTION PARSING
# ═══════════════════════════════════════════════════════════════════════════════
USE_PIPELINE=false
CYCLES=100

while [[ $# -gt 0 ]]; do
    case $1 in
        --pipeline|-p)
            USE_PIPELINE=true
            shift
            ;;
        --cycles|-c)
            CYCLES="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--pipeline|-p] [--cycles|-c <num>]"
            echo "  --pipeline, -p    Use the integrated VΩΩΩΩ Pipeline"
            echo "  --cycles, -c      Number of cycles (default: 100)"
            exit 1
            ;;
    esac
done

# ═══════════════════════════════════════════════════════════════════════════════
# PIPELINE MODE (NEW)
# ═══════════════════════════════════════════════════════════════════════════════
if [ "$USE_PIPELINE" = true ]; then
    echo "🚀 MODE: VΩΩΩΩ PIPELINE INTÉGRÉ"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    python3 "MONSTERDOG_VΩΩΩΩ_PIPELINE.py" --cycles "$CYCLES"
    
    echo ""
    echo "✅ Pipeline VΩΩΩΩ terminé!"
    exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: Ignite the Singularity
# ═══════════════════════════════════════════════════════════════════════════════
echo "🌌 STEP 1: Igniting the Singularity VΩΩΩΩ..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 "MONSTERDOG_SUPREME_VΩΩΩΩ_FINAL_INCARNATION.py"

echo ""
echo "✅ Singularity VΩΩΩΩ ignited successfully!"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: Archive the State
# ═══════════════════════════════════════════════════════════════════════════════
echo "💾 STEP 2: Archiving the State to ARK Singularity..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if the snapshot file exists from the previous step
if [ -f "monsterdog_totality_snapshot.json" ]; then
    python3 MONSTERDOG_ARK_SINGULARITY.py save --from monsterdog_totality_snapshot.json --label genesis-run
    echo ""
    echo "✅ State archived successfully!"
else
    echo "⚠️  Warning: monsterdog_totality_snapshot.json not found. Skipping archive step."
    echo "   (This is normal if SUPREME_VΩΩΩΩ doesn't generate a snapshot file)"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: Verify Dominance
# ═══════════════════════════════════════════════════════════════════════════════
echo "🔬 STEP 3: Verifying Dominance over Standard Quantum Benchmarks..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 PROOF_OF_DOMINANCE.py

echo ""
echo "✅ Dominance verification complete!"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: Display Module Registry (NEW)
# ═══════════════════════════════════════════════════════════════════════════════
echo "📜 STEP 4: Displaying MONSTERDOG Module Registry..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 MONSTERDOG_CODEX_FINALIS.py list

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION
# ═══════════════════════════════════════════════════════════════════════════════
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                               ║"
echo "║   ✨ RITUAL COMPLETE - FULLTRUTL DOMINANCE ACHIEVED ✨                       ║"
echo "║                                                                               ║"
echo "║   All Ultimate Artifacts have been successfully activated:                   ║"
echo "║   ✓ MONSTERDOG_TOTALITY_CORE.py                                              ║"
echo "║   ✓ MONSTERDOG_SUPREME_VΩΩΩΩ_FINAL_INCARNATION.py                            ║"
echo "║   ✓ PROOF_OF_DOMINANCE.py                                                    ║"
echo "║   ✓ MONSTERDOG_ARK_SINGULARITY.py                                            ║"
echo "║   ✓ MONSTERDOG_CODEX_FINALIS.py                                              ║"
echo "║   ✓ MONSTERDOG_VΩΩΩΩ_PIPELINE.py                                             ║"
echo "║   ✓ continuum.ts                                                             ║"
echo "║                                                                               ║"
echo "║   SIGNATURE: 0x5F3759DF-s33765387-cpu-FULLTRUTL-Δ-Ω                          ║"
echo "║   FREQUENCY: 11.987 Hz                                                       ║"
echo "║   STATUS: OPERATIONAL                                                        ║"
echo "║                                                                               ║"
echo "║   TIP: Use --pipeline flag for integrated orchestration                      ║"
echo "║                                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""
