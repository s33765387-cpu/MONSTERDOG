package core

import (
	"testing"
	"time"
)

func TestNewMonsterDog(t *testing.T) {
	md := NewMonsterDog()

	if md == nil {
		t.Fatal("NewMonsterDog returned nil")
	}

	if md.version != "V_OMEGA_∞" {
		t.Errorf("Expected version V_OMEGA_∞, got %s", md.version)
	}

	if md.initialized {
		t.Error("MonsterDog should not be initialized on creation")
	}
}

func TestInitialize(t *testing.T) {
	md := NewMonsterDog()

	err := md.Initialize()
	if err != nil {
		t.Fatalf("Initialize failed: %v", err)
	}

	if !md.IsInitialized() {
		t.Error("MonsterDog should be initialized")
	}

	// Test double initialization
	err = md.Initialize()
	if err == nil {
		t.Error("Expected error on double initialization")
	}
}

func TestGetVersion(t *testing.T) {
	md := NewMonsterDog()
	version := md.GetVersion()

	if version != "V_OMEGA_∞" {
		t.Errorf("Expected version V_OMEGA_∞, got %s", version)
	}
}

func TestProcess(t *testing.T) {
	md := NewMonsterDog()
	md.Initialize()

	initialCount := md.GetProcessingCount()

	md.Process()

	newCount := md.GetProcessingCount()
	if newCount != initialCount+1 {
		t.Errorf("Expected processing count to increase by 1, got %d", newCount-initialCount)
	}
}

func TestGetUptime(t *testing.T) {
	md := NewMonsterDog()

	// Before initialization, uptime should be 0
	uptime := md.GetUptime()
	if uptime != 0 {
		t.Errorf("Expected uptime 0 before initialization, got %v", uptime)
	}

	md.Initialize()
	time.Sleep(100 * time.Millisecond)

	uptime = md.GetUptime()
	if uptime < 100*time.Millisecond {
		t.Errorf("Expected uptime >= 100ms, got %v", uptime)
	}
}

func TestRegisterModule(t *testing.T) {
	md := NewMonsterDog()

	// Create a mock module
	mockModule := &mockModule{name: "test-module"}

	err := md.RegisterModule(mockModule)
	if err != nil {
		t.Fatalf("Failed to register module: %v", err)
	}

	// Try to register the same module again
	err = md.RegisterModule(mockModule)
	if err == nil {
		t.Error("Expected error when registering duplicate module")
	}
}

func TestGetModuleStatus(t *testing.T) {
	md := NewMonsterDog()

	mockModule := &mockModule{name: "test-module", status: "active"}
	md.RegisterModule(mockModule)

	status := md.GetModuleStatus()

	if len(status) != 1 {
		t.Errorf("Expected 1 module status, got %d", len(status))
	}

	if status["test-module"] != "active" {
		t.Errorf("Expected module status 'active', got '%s'", status["test-module"])
	}
}

// Mock module for testing
type mockModule struct {
	name   string
	status string
}

func (m *mockModule) Name() string {
	return m.name
}

func (m *mockModule) Initialize() error {
	return nil
}

func (m *mockModule) Status() string {
	return m.status
}
