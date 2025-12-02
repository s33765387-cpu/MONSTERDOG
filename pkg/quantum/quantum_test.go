package quantum

import (
	"testing"
)

func TestNewQuantumProcessor(t *testing.T) {
	qp := NewQuantumProcessor()

	if qp == nil {
		t.Fatal("NewQuantumProcessor returned nil")
	}

	if qp.initialized {
		t.Error("QuantumProcessor should not be initialized on creation")
	}

	if qp.qubits != 8 {
		t.Errorf("Expected 8 qubits, got %d", qp.qubits)
	}
}

func TestInitialize(t *testing.T) {
	qp := NewQuantumProcessor()

	err := qp.Initialize()
	if err != nil {
		t.Fatalf("Initialize failed: %v", err)
	}

	state := qp.GetQuantumState()
	if state.Coherence != 1.0 {
		t.Errorf("Expected coherence 1.0, got %f", state.Coherence)
	}
	if state.Entanglement != 0.0 {
		t.Errorf("Expected entanglement 0.0, got %f", state.Entanglement)
	}
	if state.Superposition != 0.5 {
		t.Errorf("Expected superposition 0.5, got %f", state.Superposition)
	}
	if state.Energy != 1.0 {
		t.Errorf("Expected energy 1.0, got %f", state.Energy)
	}

	// Test double initialization
	err = qp.Initialize()
	if err == nil {
		t.Error("Expected error on double initialization")
	}
}

func TestApplyHadamard(t *testing.T) {
	qp := NewQuantumProcessor()
	qp.Initialize()

	initialState := qp.GetQuantumState()

	err := qp.ApplyHadamard(0)
	if err != nil {
		t.Fatalf("ApplyHadamard failed: %v", err)
	}

	newState := qp.GetQuantumState()
	if newState.Superposition <= initialState.Superposition {
		t.Error("Superposition should increase after Hadamard gate")
	}

	// Test invalid qubit index
	err = qp.ApplyHadamard(100)
	if err == nil {
		t.Error("Expected error for invalid qubit index")
	}
}

func TestEntanglQubits(t *testing.T) {
	qp := NewQuantumProcessor()
	qp.Initialize()

	initialState := qp.GetQuantumState()

	err := qp.EntanglQubits(0, 1)
	if err != nil {
		t.Fatalf("EntanglQubits failed: %v", err)
	}

	newState := qp.GetQuantumState()
	if newState.Entanglement <= initialState.Entanglement {
		t.Error("Entanglement should increase after entangling qubits")
	}

	// Test invalid qubit indices
	err = qp.EntanglQubits(100, 200)
	if err == nil {
		t.Error("Expected error for invalid qubit indices")
	}

	// Test negative indices
	err = qp.EntanglQubits(-1, 0)
	if err == nil {
		t.Error("Expected error for negative qubit index")
	}

	// Test entangling qubit with itself
	err = qp.EntanglQubits(0, 0)
	if err == nil {
		t.Error("Expected error for entangling qubit with itself")
	}
}

func TestMeasure(t *testing.T) {
	qp := NewQuantumProcessor()
	qp.Initialize()

	initialCoherence := qp.GetQuantumState().Coherence

	result, err := qp.Measure(0)
	if err != nil {
		t.Fatalf("Measure failed: %v", err)
	}

	if result != 0 && result != 1 {
		t.Errorf("Expected measurement result 0 or 1, got %d", result)
	}

	newCoherence := qp.GetQuantumState().Coherence
	if newCoherence >= initialCoherence {
		t.Error("Coherence should decrease after measurement")
	}

	// Test invalid qubit index
	_, err = qp.Measure(100)
	if err == nil {
		t.Error("Expected error for invalid qubit index")
	}
}

func TestProcessQuantumAlgorithm(t *testing.T) {
	qp := NewQuantumProcessor()
	qp.Initialize()

	tests := []struct {
		algorithm string
		wantErr   bool
	}{
		{"GROVER", false},
		{"SHOR", false},
		{"QFT", false},
		{"INVALID", true},
	}

	for _, tt := range tests {
		t.Run(tt.algorithm, func(t *testing.T) {
			result, err := qp.ProcessQuantumAlgorithm(tt.algorithm)

			if tt.wantErr {
				if err == nil {
					t.Error("Expected error for invalid algorithm")
				}
			} else {
				if err != nil {
					t.Errorf("ProcessQuantumAlgorithm failed: %v", err)
				}
				if result < 0 {
					t.Errorf("Expected non-negative result, got %f", result)
				}
			}
		})
	}
}

func TestResetState(t *testing.T) {
	qp := NewQuantumProcessor()
	qp.Initialize()

	// Modify state
	qp.ApplyHadamard(0)
	qp.EntanglQubits(0, 1)
	qp.Measure(0)

	// Reset
	qp.ResetState()

	state := qp.GetQuantumState()
	if state.Coherence != 1.0 {
		t.Errorf("Expected coherence 1.0 after reset, got %f", state.Coherence)
	}
	if state.Entanglement != 0.0 {
		t.Errorf("Expected entanglement 0.0 after reset, got %f", state.Entanglement)
	}
	if state.Superposition != 0.5 {
		t.Errorf("Expected superposition 0.5 after reset, got %f", state.Superposition)
	}
	if state.Energy != 1.0 {
		t.Errorf("Expected energy 1.0 after reset, got %f", state.Energy)
	}
}

func TestGetQubitCount(t *testing.T) {
	qp := NewQuantumProcessor()

	count := qp.GetQubitCount()
	if count != 8 {
		t.Errorf("Expected 8 qubits, got %d", count)
	}
}

func TestNewQubit(t *testing.T) {
	qubit := NewQubit()

	// Qubit should be in |0⟩ state
	if real(qubit.alpha) != 1.0 || imag(qubit.alpha) != 0.0 {
		t.Errorf("Expected alpha = (1+0i), got %v", qubit.alpha)
	}
	if real(qubit.beta) != 0.0 || imag(qubit.beta) != 0.0 {
		t.Errorf("Expected beta = (0+0i), got %v", qubit.beta)
	}
}

func TestQubitMeasure(t *testing.T) {
	qubit := NewQubit()

	result := qubit.Measure()
	if result != 0 && result != 1 {
		t.Errorf("Expected measurement result 0 or 1, got %d", result)
	}

	// After measurement, qubit should be in collapsed state
	// Either |0⟩ or |1⟩
	if result == 0 {
		if real(qubit.alpha) != 1.0 {
			t.Error("Qubit should be in |0⟩ state after measuring 0")
		}
	} else {
		if real(qubit.beta) != 1.0 {
			t.Error("Qubit should be in |1⟩ state after measuring 1")
		}
	}
}
