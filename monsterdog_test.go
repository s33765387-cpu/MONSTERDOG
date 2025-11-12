package main

import (
	"encoding/json"
	"math"
	"testing"
	"time"
)

// TestStateVectorCreation teste la création d'un StateVector
func TestStateVectorCreation(t *testing.T) {
	sv := StateVector{
		Timestamp:   time.Now().UTC().Format(time.RFC3339Nano),
		CycleID:     1,
		Mode:        "FULLTRUTL-Δ-Ω",
		Coherence:   0.99995,
		Entropy:     0.00005,
		ResonanceHz: 11.987,
		Drift:       0.0,
		Seal:        SignatureUniversal,
	}

	if sv.CycleID != 1 {
		t.Errorf("Expected CycleID 1, got %d", sv.CycleID)
	}

	if sv.Mode != "FULLTRUTL-Δ-Ω" {
		t.Errorf("Expected Mode 'FULLTRUTL-Δ-Ω', got %s", sv.Mode)
	}

	if sv.Seal != SignatureUniversal {
		t.Errorf("Expected Seal '%s', got %s", SignatureUniversal, sv.Seal)
	}
}

// TestStateVectorJSON teste la sérialisation JSON
func TestStateVectorJSON(t *testing.T) {
	sv := StateVector{
		Timestamp:   "2025-11-12T00:00:00Z",
		CycleID:     1,
		Mode:        "FULLTRUTL-Δ-Ω",
		Coherence:   0.99995,
		Entropy:     0.00005,
		ResonanceHz: 11.987,
		Drift:       0.0,
		Seal:        SignatureUniversal,
	}

	jsonStr, err := sv.ToJSON()
	if err != nil {
		t.Fatalf("Failed to marshal StateVector: %v", err)
	}

	// Vérifier que le JSON peut être décodé
	var decoded StateVector
	err = json.Unmarshal([]byte(jsonStr), &decoded)
	if err != nil {
		t.Fatalf("Failed to unmarshal StateVector: %v", err)
	}

	if decoded.CycleID != sv.CycleID {
		t.Errorf("Expected CycleID %d, got %d", sv.CycleID, decoded.CycleID)
	}
}

// TestStateVectorChecksum teste le calcul du checksum
func TestStateVectorChecksum(t *testing.T) {
	sv := StateVector{
		Timestamp:   "2025-11-12T00:00:00Z",
		CycleID:     1,
		Mode:        "FULLTRUTL-Δ-Ω",
		Coherence:   0.99995,
		Entropy:     0.00005,
		ResonanceHz: 11.987,
		Drift:       0.0,
		Seal:        SignatureUniversal,
	}

	checksum := sv.ComputeChecksum()

	if len(checksum) != 128 { // SHA512 produit 128 caractères hex
		t.Errorf("Expected checksum length 128, got %d", len(checksum))
	}

	// Vérifier que le checksum est reproductible
	checksum2 := sv.ComputeChecksum()
	if checksum != checksum2 {
		t.Errorf("Checksum should be reproducible")
	}
}

// TestFractalMetricEngineCreation teste la création du moteur
func TestFractalMetricEngineCreation(t *testing.T) {
	engine := NewFractalMetricEngine(UniversalSeed)

	if engine == nil {
		t.Fatal("Failed to create FractalMetricEngine")
	}

	if len(engine.CoherenceHistory) != 0 {
		t.Errorf("Expected empty CoherenceHistory, got %d elements", len(engine.CoherenceHistory))
	}

	if engine.MaxHistory != 100 {
		t.Errorf("Expected MaxHistory 100, got %d", engine.MaxHistory)
	}
}

// TestFractalMetricEngineCompute teste le calcul des métriques
func TestFractalMetricEngineCompute(t *testing.T) {
	engine := NewFractalMetricEngine(UniversalSeed)

	metrics := engine.ComputeMetrics(1)

	// Vérifier que toutes les métriques sont présentes
	if _, ok := metrics["coherence"]; !ok {
		t.Error("Missing 'coherence' metric")
	}
	if _, ok := metrics["entropy"]; !ok {
		t.Error("Missing 'entropy' metric")
	}
	if _, ok := metrics["resonance_hz"]; !ok {
		t.Error("Missing 'resonance_hz' metric")
	}
	if _, ok := metrics["drift"]; !ok {
		t.Error("Missing 'drift' metric")
	}

	// Vérifier les valeurs
	coherence := metrics["coherence"]
	if coherence < 0 || coherence > 1 {
		t.Errorf("Coherence should be between 0 and 1, got %f", coherence)
	}

	entropy := metrics["entropy"]
	if entropy < 0 || entropy > 1 {
		t.Errorf("Entropy should be between 0 and 1, got %f", entropy)
	}

	// Vérifier que coherence + entropy ≈ 1
	sum := coherence + entropy
	if math.Abs(sum-1.0) > 0.00001 {
		t.Errorf("Coherence + Entropy should be approximately 1.0, got %f", sum)
	}

	resonance := metrics["resonance_hz"]
	if resonance < BaseFrequency-10 || resonance > BaseFrequency+10 {
		t.Errorf("Resonance should be around %f, got %f", BaseFrequency, resonance)
	}
}

// TestFractalMetricEngineHistory teste l'historique des métriques
func TestFractalMetricEngineHistory(t *testing.T) {
	engine := NewFractalMetricEngine(UniversalSeed)

	// Générer plusieurs métriques
	for i := int64(1); i <= 150; i++ {
		engine.ComputeMetrics(i)
	}

	// Vérifier que l'historique ne dépasse pas MaxHistory
	if len(engine.CoherenceHistory) > engine.MaxHistory {
		t.Errorf("CoherenceHistory should not exceed MaxHistory (%d), got %d",
			engine.MaxHistory, len(engine.CoherenceHistory))
	}

	if len(engine.EntropyHistory) > engine.MaxHistory {
		t.Errorf("EntropyHistory should not exceed MaxHistory (%d), got %d",
			engine.MaxHistory, len(engine.EntropyHistory))
	}

	// Vérifier que l'historique contient des valeurs
	if len(engine.CoherenceHistory) == 0 {
		t.Error("CoherenceHistory should not be empty")
	}
}

// TestMonsterDogDaemonCreation teste la création du daemon
func TestMonsterDogDaemonCreation(t *testing.T) {
	daemon := NewMonsterDogDaemon()

	if daemon == nil {
		t.Fatal("Failed to create MonsterDogDaemon")
	}

	if daemon.cycleCount != 0 {
		t.Errorf("Expected initial cycleCount 0, got %d", daemon.cycleCount)
	}

	if daemon.running {
		t.Error("Daemon should not be running initially")
	}

	if daemon.engine == nil {
		t.Error("Daemon should have a FractalMetricEngine")
	}
}

// TestMonsterDogDaemonGenerateStateVector teste la génération de vecteurs d'état
func TestMonsterDogDaemonGenerateStateVector(t *testing.T) {
	daemon := NewMonsterDogDaemon()

	sv := daemon.GenerateStateVector()

	if sv.CycleID != 1 {
		t.Errorf("Expected first CycleID to be 1, got %d", sv.CycleID)
	}

	if sv.Mode != "FULLTRUTL-Δ-Ω" {
		t.Errorf("Expected Mode 'FULLTRUTL-Δ-Ω', got %s", sv.Mode)
	}

	if sv.Seal != SignatureUniversal {
		t.Errorf("Expected Seal '%s', got %s", SignatureUniversal, sv.Seal)
	}

	if sv.ChecksumSHA512 == "" {
		t.Error("ChecksumSHA512 should not be empty")
	}

	// Générer un second vecteur
	sv2 := daemon.GenerateStateVector()

	if sv2.CycleID != 2 {
		t.Errorf("Expected second CycleID to be 2, got %d", sv2.CycleID)
	}
}

// TestMonsterDogDaemonStats teste les statistiques du daemon
func TestMonsterDogDaemonStats(t *testing.T) {
	daemon := NewMonsterDogDaemon()

	// Générer quelques vecteurs
	for i := 0; i < 5; i++ {
		daemon.GenerateStateVector()
	}

	stats := daemon.GetStats()

	cycleCount, ok := stats["cycle_count"].(int64)
	if !ok || cycleCount != 5 {
		t.Errorf("Expected cycle_count 5, got %v", stats["cycle_count"])
	}

	signature, ok := stats["signature"].(string)
	if !ok || signature != SignatureUniversal {
		t.Errorf("Expected signature '%s', got %v", SignatureUniversal, stats["signature"])
	}

	baseFreq, ok := stats["base_frequency"].(float64)
	if !ok || baseFreq != BaseFrequency {
		t.Errorf("Expected base_frequency %f, got %v", BaseFrequency, stats["base_frequency"])
	}
}

// TestCalculateVariance teste la fonction de calcul de variance
func TestCalculateVariance(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{
			name:     "Empty slice",
			values:   []float64{},
			expected: 0.0,
		},
		{
			name:     "Single value",
			values:   []float64{5.0},
			expected: 0.0,
		},
		{
			name:     "Identical values",
			values:   []float64{3.0, 3.0, 3.0},
			expected: 0.0,
		},
		{
			name:     "Simple variance",
			values:   []float64{1.0, 2.0, 3.0, 4.0, 5.0},
			expected: 2.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calculateVariance(tt.values)
			if math.Abs(result-tt.expected) > 0.0001 {
				t.Errorf("Expected variance %f, got %f", tt.expected, result)
			}
		})
	}
}

// TestFindMinMax teste la fonction de recherche min/max
func TestFindMinMax(t *testing.T) {
	tests := []struct {
		name        string
		values      []float64
		expectedMin float64
		expectedMax float64
	}{
		{
			name:        "Empty slice",
			values:      []float64{},
			expectedMin: 0.0,
			expectedMax: 0.0,
		},
		{
			name:        "Single value",
			values:      []float64{5.0},
			expectedMin: 5.0,
			expectedMax: 5.0,
		},
		{
			name:        "Multiple values",
			values:      []float64{3.0, 1.0, 4.0, 1.5, 9.0, 2.6},
			expectedMin: 1.0,
			expectedMax: 9.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			min, max := findMinMax(tt.values)
			if min != tt.expectedMin {
				t.Errorf("Expected min %f, got %f", tt.expectedMin, min)
			}
			if max != tt.expectedMax {
				t.Errorf("Expected max %f, got %f", tt.expectedMax, max)
			}
		})
	}
}

// TestRoundFloat teste la fonction d'arrondi
func TestRoundFloat(t *testing.T) {
	tests := []struct {
		name      string
		value     float64
		precision int
		expected  float64
	}{
		{
			name:      "Round to 2 decimals",
			value:     3.14159,
			precision: 2,
			expected:  3.14,
		},
		{
			name:      "Round to 4 decimals",
			value:     3.14159,
			precision: 4,
			expected:  3.1416,
		},
		{
			name:      "Round to 0 decimals",
			value:     3.7,
			precision: 0,
			expected:  4.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := roundFloat(tt.value, tt.precision)
			if result != tt.expected {
				t.Errorf("Expected %f, got %f", tt.expected, result)
			}
		})
	}
}

// TestConcurrentStateVectorGeneration teste la génération concurrente
func TestConcurrentStateVectorGeneration(t *testing.T) {
	daemon := NewMonsterDogDaemon()

	// Générer des vecteurs d'état de manière concurrente
	done := make(chan bool)
	numGoroutines := 10
	vectorsPerGoroutine := 10

	for i := 0; i < numGoroutines; i++ {
		go func() {
			for j := 0; j < vectorsPerGoroutine; j++ {
				daemon.GenerateStateVector()
			}
			done <- true
		}()
	}

	// Attendre que toutes les goroutines se terminent
	for i := 0; i < numGoroutines; i++ {
		<-done
	}

	stats := daemon.GetStats()
	cycleCount := stats["cycle_count"].(int64)
	expectedCycles := int64(numGoroutines * vectorsPerGoroutine)

	if cycleCount != expectedCycles {
		t.Errorf("Expected %d cycles, got %d", expectedCycles, cycleCount)
	}
}
