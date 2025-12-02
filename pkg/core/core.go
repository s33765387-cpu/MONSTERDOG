// Package core provides the core MONSTERDOG functionality
package core

import (
	"fmt"
	"sync"
	"time"
)

// MonsterDog represents the core MONSTERDOG system
type MonsterDog struct {
	version         string
	initialized     bool
	startTime       time.Time
	processingCount uint64
	mu              sync.RWMutex
	modules         map[string]Module
}

// Module represents a MONSTERDOG module
type Module interface {
	Name() string
	Initialize() error
	Status() string
}

// NewMonsterDog creates a new MONSTERDOG instance
func NewMonsterDog() *MonsterDog {
	return &MonsterDog{
		version:     "V_OMEGA_∞",
		modules:     make(map[string]Module),
		initialized: false,
	}
}

// Initialize initializes the MONSTERDOG core system
func (m *MonsterDog) Initialize() error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if m.initialized {
		return fmt.Errorf("MONSTERDOG already initialized")
	}

	m.startTime = time.Now()
	m.initialized = true

	return nil
}

// Process performs one processing cycle
func (m *MonsterDog) Process() {
	m.mu.Lock()
	m.processingCount++
	m.mu.Unlock()

	// Simulate processing
	time.Sleep(100 * time.Millisecond)
}

// GetVersion returns the MONSTERDOG version
func (m *MonsterDog) GetVersion() string {
	return m.version
}

// GetUptime returns the system uptime
func (m *MonsterDog) GetUptime() time.Duration {
	m.mu.RLock()
	defer m.mu.RUnlock()

	if !m.initialized {
		return 0
	}

	return time.Since(m.startTime)
}

// GetProcessingCount returns the total number of processing cycles
func (m *MonsterDog) GetProcessingCount() uint64 {
	m.mu.RLock()
	defer m.mu.RUnlock()

	return m.processingCount
}

// RegisterModule registers a module with MONSTERDOG
func (m *MonsterDog) RegisterModule(module Module) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	name := module.Name()
	if _, exists := m.modules[name]; exists {
		return fmt.Errorf("module %s already registered", name)
	}

	m.modules[name] = module
	return nil
}

// GetModuleStatus returns the status of all registered modules
func (m *MonsterDog) GetModuleStatus() map[string]string {
	m.mu.RLock()
	defer m.mu.RUnlock()

	status := make(map[string]string)
	for name, module := range m.modules {
		status[name] = module.Status()
	}

	return status
}

// IsInitialized returns whether MONSTERDOG is initialized
func (m *MonsterDog) IsInitialized() bool {
	m.mu.RLock()
	defer m.mu.RUnlock()

	return m.initialized
}
