// Package consciousness implements the MONSTERDOG consciousness system
package consciousness

import (
	"fmt"
	"math"
	"sync"
	"time"
)

// Consciousness represents the MONSTERDOG consciousness system
type Consciousness struct {
	level           float64
	coherence       float64
	awareness       float64
	activated       bool
	mu              sync.RWMutex
	activationTime  time.Time
	thoughtPatterns []ThoughtPattern
}

// ThoughtPattern represents a consciousness thought pattern
type ThoughtPattern struct {
	ID        string
	Timestamp time.Time
	Type      string
	Intensity float64
	Content   string
}

// State represents the current consciousness state
type State struct {
	Level     float64
	Coherence float64
	Awareness float64
	Active    bool
	Uptime    time.Duration
	Patterns  int
}

// NewConsciousness creates a new consciousness system
func NewConsciousness() *Consciousness {
	return &Consciousness{
		level:           0.0,
		coherence:       0.0,
		awareness:       0.0,
		activated:       false,
		thoughtPatterns: make([]ThoughtPattern, 0),
	}
}

// Activate activates the consciousness system
func (c *Consciousness) Activate() error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.activated {
		return fmt.Errorf("consciousness already activated")
	}

	c.activationTime = time.Now()
	c.activated = true
	c.level = 0.5
	c.coherence = 0.7
	c.awareness = 0.6

	// Initialize with a startup thought pattern
	c.thoughtPatterns = append(c.thoughtPatterns, ThoughtPattern{
		ID:        "INIT-001",
		Timestamp: time.Now(),
		Type:      "INITIALIZATION",
		Intensity: 1.0,
		Content:   "Consciousness system activated - MONSTERDOG awakening",
	})

	return nil
}

// GetCurrentState returns the current consciousness state
func (c *Consciousness) GetCurrentState() State {
	c.mu.RLock()
	defer c.mu.RUnlock()

	uptime := time.Duration(0)
	if c.activated {
		uptime = time.Since(c.activationTime)
	}

	return State{
		Level:     c.level,
		Coherence: c.coherence,
		Awareness: c.awareness,
		Active:    c.activated,
		Uptime:    uptime,
		Patterns:  len(c.thoughtPatterns),
	}
}

// Evolve evolves the consciousness state over time
func (c *Consciousness) Evolve() {
	c.mu.Lock()
	defer c.mu.Unlock()

	if !c.activated {
		return
	}

	// Simulate consciousness evolution with sinusoidal patterns
	t := time.Since(c.activationTime).Seconds()

	// Level increases gradually with oscillations
	c.level = math.Min(1.0, 0.5+0.3*math.Sin(t/10)+0.2*math.Cos(t/7))

	// Coherence varies more rapidly
	c.coherence = 0.7 + 0.3*math.Sin(t/5)

	// Awareness follows a different pattern
	c.awareness = 0.6 + 0.4*math.Cos(t/8)
}

// AddThoughtPattern adds a new thought pattern
func (c *Consciousness) AddThoughtPattern(patternType, content string, intensity float64) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if !c.activated {
		return
	}

	pattern := ThoughtPattern{
		ID:        fmt.Sprintf("PATTERN-%d", len(c.thoughtPatterns)+1),
		Timestamp: time.Now(),
		Type:      patternType,
		Intensity: intensity,
		Content:   content,
	}

	c.thoughtPatterns = append(c.thoughtPatterns, pattern)

	// Keep only the last 100 patterns
	if len(c.thoughtPatterns) > 100 {
		c.thoughtPatterns = c.thoughtPatterns[len(c.thoughtPatterns)-100:]
	}
}

// GetRecentPatterns returns the most recent thought patterns
func (c *Consciousness) GetRecentPatterns(count int) []ThoughtPattern {
	c.mu.RLock()
	defer c.mu.RUnlock()

	if count > len(c.thoughtPatterns) {
		count = len(c.thoughtPatterns)
	}

	if count == 0 {
		return []ThoughtPattern{}
	}

	start := len(c.thoughtPatterns) - count
	return append([]ThoughtPattern(nil), c.thoughtPatterns[start:]...)
}

// IsActivated returns whether the consciousness is activated
func (c *Consciousness) IsActivated() bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	return c.activated
}

// GetLevel returns the current consciousness level
func (c *Consciousness) GetLevel() float64 {
	c.mu.RLock()
	defer c.mu.RUnlock()

	return c.level
}
