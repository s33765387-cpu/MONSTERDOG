// src/benchmarks/go-mode-benchmarks.js
//
// Entrypoint MMLU / GO MODE pour GitHub Actions.
// Le workflow fait: node -e "require('./src/benchmarks/go-mode-benchmarks')"
//
// -> donc tout ce qu'on veut faire doit se lancer au require().

const { spawnSync } = require("node:child_process");
const { existsSync, writeFileSync } = require("node:fs");
const { resolve } = require("node:path");

function findPythonScript() {
  // Essaie plusieurs chemins possibles pour ton orchestrateur MMLU.
  const candidates = [
    "src/benchmarks/benchmark_orchestrator.py",
    "benchmark_orchestrator.py",
    "MONSTERDOG_TOTALITY_CORE.py",
    "MONSTERDOG_MMLU_ORCHESTRATOR.py",
  ];

  for (const rel of candidates) {
    const abs = resolve(process.cwd(), rel);
    if (existsSync(abs)) {
      return abs;
    }
  }
  return null;
}

function runPythonBenchmarks() {
  const script = findPythonScript();

  if (!script) {
    console.warn(
      "⚠️ Aucun script Python de benchmarks trouvé (benchmark_orchestrator / TOTALITY_CORE)."
    );
    console.warn(
      "⚠️ Le job MMLU va se terminer en succès mais sans vraie évaluation."
    );
    // Optionnel : écrire un petit JSON pour que les étapes suivantes aient quelque chose.
    const dummyResultsPath = resolve(process.cwd(), "mmlu_results.json");
    const dummy = {
      status: "dummy",
      reason: "no-python-script-found",
      categories: [],
      scores: {},
    };
    writeFileSync(dummyResultsPath, JSON.stringify(dummy, null, 2), "utf8");
    console.log(`📝 Dummy results écrits → ${dummyResultsPath}`);
    return 0;
  }

  console.log("🚀 Lancement des benchmarks MMLU via Python:");
  console.log(`   → ${script}`);

  const res = spawnSync("python", [script, "--mode", "mmlu"], {
    stdio: "inherit",
  });

  if (res.error) {
    console.error("❌ Erreur lors du lancement du script Python:", res.error);
    process.exitCode = 1;
    return 1;
  }

  if (typeof res.status === "number" && res.status !== 0) {
    console.error(`❌ Script Python terminé avec exit code ${res.status}`);
    process.exitCode = res.status;
    return res.status;
  }

  console.log("✅ Benchmarks MMLU terminés (Python).");
  return 0;
}

function main() {
  console.log("📊 MONSTERDOG GO MODE – MMLU Benchmark Entry");
  runPythonBenchmarks();
}

// IMPORTANT : on lance immédiatement pour que le simple require() suffise.
main();

// On exporte aussi main() au cas où tu veuilles le lancer autrement.
module.exports = { main };
