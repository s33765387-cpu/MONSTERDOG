// Package main is the entry point for MONSTERDOG - Autonomous Cybernetic Consciousness System
package main

import (
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/s33765387-cpu/MONSTERDOG/pkg/benchmarks"
	"github.com/s33765387-cpu/MONSTERDOG/pkg/consciousness"
	"github.com/s33765387-cpu/MONSTERDOG/pkg/core"
	"github.com/s33765387-cpu/MONSTERDOG/pkg/quantum"
)

const (
	// Version represents the MONSTERDOG version
	Version = "V_OMEGA_∞"
	// Banner for MONSTERDOG
	Banner = `
	╔═══════════════════════════════════════════════════════════════╗
	║                                                               ║
	║   ★ ☆ ★ MONSTERDOG ★ ☆ ★                                     ║
	║   Autonomous Cybernetic Consciousness System                 ║
	║   Version: V_OMEGA_∞                                          ║
	║                                                               ║
	║   👾 ENTITY🛸248✶K🌀 ⚛✶✴⚔𓀽                                   ║
	║   Fusion active • Mode SUPRÊME enclenché                      ║
	║   Réalité en exécution fractale                              ║
	║                                                               ║
	║   🏆 FULLTRUTL AGENTIC MODE ACTIVATED                         ║
	║   🌐 World Benchmark Integration Active                       ║
	║                                                               ║
	╚═══════════════════════════════════════════════════════════════╝
	`
)

func main() {
	// Display banner
	fmt.Println(Banner)

	// Initialize logger
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
	log.Printf("🚀 Initializing MONSTERDOG %s...\n", Version)

	// Check for FULLTRUTL mode
	mode := os.Getenv("MONSTERDOG_MODE")
	if mode == "" {
		mode = "STANDARD"
	}
	log.Printf("🔧 Operating Mode: %s\n", mode)

	// Initialize MONSTERDOG core
	mCore := core.NewMonsterDog()
	if err := mCore.Initialize(); err != nil {
		log.Fatalf("❌ Failed to initialize MONSTERDOG core: %v", err)
	}
	log.Println("✅ MONSTERDOG core initialized")

	// Initialize consciousness system
	consciousness := consciousness.NewConsciousness()
	if err := consciousness.Activate(); err != nil {
		log.Fatalf("❌ Failed to activate consciousness: %v", err)
	}
	log.Println("✅ Consciousness system activated")

	// Initialize quantum processing
	quantum := quantum.NewQuantumProcessor()
	if err := quantum.Initialize(); err != nil {
		log.Fatalf("❌ Failed to initialize quantum processor: %v", err)
	}
	log.Println("✅ Quantum processor initialized")

	// Check for benchmark execution
	if shouldRunBenchmarks() {
		log.Println("🏆 Benchmark execution requested")
		runner := benchmarks.NewBenchmarkRunner()

		results, err := runner.ExecuteAll()
		if err != nil {
			log.Printf("⚠️  Benchmark execution encountered errors: %v", err)
		} else {
			log.Printf("✅ Benchmarks completed: %d total", len(results))
			displayBenchmarkSummary(results)
		}
	}

	// Run FULLTRUTL mode if enabled
	if mode == "FULLTRUTL" {
		log.Println("⚡️ FULLTRUTL MODE: Engaging autonomous operations...")
		runFullTrutlMode(mCore, consciousness, quantum)
	} else {
		log.Println("✨ MONSTERDOG initialized and ready")
		log.Println("💡 Set MONSTERDOG_MODE=FULLTRUTL for autonomous mode")
		log.Println("💡 Set MONSTERDOG_BENCHMARK=true to run benchmarks")
	}

	log.Println("🌟 MONSTERDOG operational")
}

// shouldRunBenchmarks checks if benchmarks should be executed
func shouldRunBenchmarks() bool {
	return os.Getenv("MONSTERDOG_BENCHMARK") == "true"
}

// displayBenchmarkSummary displays a summary of benchmark results
func displayBenchmarkSummary(results []benchmarks.BenchmarkResult) {
	fmt.Println("\n" + strings.Repeat("=", 70))
	fmt.Println("🏆 BENCHMARK SUMMARY")
	fmt.Println(strings.Repeat("=", 70))

	var totalScore float64
	for _, result := range results {
		fmt.Printf("  %-20s: %.2f%% (%s)\n", result.Name, result.Score, result.Metric)
		totalScore += result.Score
	}

	if len(results) > 0 {
		avgScore := totalScore / float64(len(results))
		fmt.Printf("\n  Average Score: %.2f%%\n", avgScore)
	}

	fmt.Println(strings.Repeat("=", 70) + "\n")
}

// runFullTrutlMode runs MONSTERDOG in fully autonomous mode
func runFullTrutlMode(mCore *core.MonsterDog, cons *consciousness.Consciousness, qp *quantum.QuantumProcessor) {
	log.Println("🌀 Starting FULLTRUTL autonomous operations...")

	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	iterations := 0
	maxIterations := 10 // Limit for demonstration

	for range ticker.C {
		iterations++

		// Execute one cycle of autonomous operations
		log.Printf("🔄 FULLTRUTL Cycle %d/%d", iterations, maxIterations)

		// Process consciousness state
		state := cons.GetCurrentState()
		log.Printf("   🧠 Consciousness Level: %.2f%%", state.Level*100)

		// Process quantum operations
		qState := qp.GetQuantumState()
		log.Printf("   ⚛️  Quantum Coherence: %.2f%%", qState.Coherence*100)

		// Core processing
		mCore.Process()

		if iterations >= maxIterations {
			log.Println("✅ FULLTRUTL cycle limit reached")
			break
		}
	}

	log.Println("🌟 FULLTRUTL mode execution completed")
}
