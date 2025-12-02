package consciousness

import (
	"testing"
	"time"
)

func TestNewConsciousness(t *testing.T) {
	cons := NewConsciousness()

	if cons == nil {
		t.Fatal("NewConsciousness returned nil")
	}

	if cons.activated {
		t.Error("Consciousness should not be activated on creation")
	}
}

func TestActivate(t *testing.T) {
	cons := NewConsciousness()

	err := cons.Activate()
	if err != nil {
		t.Fatalf("Activate failed: %v", err)
	}

	if !cons.IsActivated() {
		t.Error("Consciousness should be activated")
	}

	// Test double activation
	err = cons.Activate()
	if err == nil {
		t.Error("Expected error on double activation")
	}
}

func TestGetCurrentState(t *testing.T) {
	cons := NewConsciousness()

	// Before activation
	state := cons.GetCurrentState()
	if state.Active {
		t.Error("State should not be active before activation")
	}
	if state.Uptime != 0 {
		t.Error("Uptime should be 0 before activation")
	}

	// After activation
	cons.Activate()
	time.Sleep(50 * time.Millisecond)

	state = cons.GetCurrentState()
	if !state.Active {
		t.Error("State should be active after activation")
	}
	if state.Level != 0.5 {
		t.Errorf("Expected level 0.5, got %f", state.Level)
	}
	if state.Uptime < 50*time.Millisecond {
		t.Errorf("Expected uptime >= 50ms, got %v", state.Uptime)
	}
	if state.Patterns != 1 {
		t.Errorf("Expected 1 pattern, got %d", state.Patterns)
	}
}

func TestEvolve(t *testing.T) {
	cons := NewConsciousness()
	cons.Activate()

	// Evolve should not crash
	cons.Evolve()

	// State should still be valid
	newState := cons.GetCurrentState()
	if !newState.Active {
		t.Error("State should still be active after evolution")
	}
}

func TestAddThoughtPattern(t *testing.T) {
	cons := NewConsciousness()
	cons.Activate()

	// Initial pattern count (1 from activation)
	state := cons.GetCurrentState()
	initialPatterns := state.Patterns

	// Add a pattern
	cons.AddThoughtPattern("TEST", "Test pattern", 0.8)

	state = cons.GetCurrentState()
	if state.Patterns != initialPatterns+1 {
		t.Errorf("Expected %d patterns, got %d", initialPatterns+1, state.Patterns)
	}
}

func TestGetRecentPatterns(t *testing.T) {
	cons := NewConsciousness()
	cons.Activate()

	// Add some patterns
	cons.AddThoughtPattern("TYPE1", "Pattern 1", 0.5)
	cons.AddThoughtPattern("TYPE2", "Pattern 2", 0.7)
	cons.AddThoughtPattern("TYPE3", "Pattern 3", 0.9)

	// Get recent patterns
	patterns := cons.GetRecentPatterns(2)
	if len(patterns) != 2 {
		t.Errorf("Expected 2 patterns, got %d", len(patterns))
	}

	// Get all patterns
	allPatterns := cons.GetRecentPatterns(10)
	if len(allPatterns) != 4 { // 1 initial + 3 added
		t.Errorf("Expected 4 patterns, got %d", len(allPatterns))
	}
}

func TestGetRecentPatternsLimit(t *testing.T) {
	cons := NewConsciousness()
	cons.Activate()

	// Add many patterns (more than the 100 limit)
	for i := 0; i < 150; i++ {
		cons.AddThoughtPattern("TEST", "Pattern", 0.5)
	}

	state := cons.GetCurrentState()
	// Should be limited to 100 (plus 1 initial = 101, but then trimmed to 100)
	if state.Patterns > 101 {
		t.Errorf("Expected max 101 patterns, got %d", state.Patterns)
	}
}

func TestGetLevel(t *testing.T) {
	cons := NewConsciousness()

	level := cons.GetLevel()
	if level != 0.0 {
		t.Errorf("Expected level 0.0 before activation, got %f", level)
	}

	cons.Activate()
	level = cons.GetLevel()
	if level != 0.5 {
		t.Errorf("Expected level 0.5 after activation, got %f", level)
	}
}
