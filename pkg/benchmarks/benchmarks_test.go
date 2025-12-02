package benchmarks

import (
	"os"
	"path/filepath"
	"testing"
)

func TestNewBenchmarkRunner(t *testing.T) {
	runner := NewBenchmarkRunner()

	if runner == nil {
		t.Fatal("NewBenchmarkRunner returned nil")
	}

	if runner.resultsDir != "benchmark_results" {
		t.Errorf("Expected resultsDir 'benchmark_results', got %s", runner.resultsDir)
	}
}

func TestExecuteAll(t *testing.T) {
	// Create a temporary directory for test results
	tmpDir := filepath.Join(os.TempDir(), "monsterdog_test_results")
	defer os.RemoveAll(tmpDir)

	runner := NewBenchmarkRunner()
	runner.resultsDir = tmpDir

	results, err := runner.ExecuteAll()
	if err != nil {
		t.Fatalf("ExecuteAll failed: %v", err)
	}

	// Should have executed all benchmarks
	if len(results) != len(OfficialBenchmarks) {
		t.Errorf("Expected %d results, got %d", len(OfficialBenchmarks), len(results))
	}

	// Verify all benchmarks have valid scores
	for _, result := range results {
		if result.Score < 0 || result.Score > 100 {
			t.Errorf("Invalid score for %s: %f", result.Name, result.Score)
		}
		if result.Metric == "" {
			t.Errorf("Missing metric for %s", result.Name)
		}
		if result.LeaderboardURL == "" {
			t.Errorf("Missing leaderboard URL for %s", result.Name)
		}
	}

	// Verify results file was created
	summaryPath := filepath.Join(tmpDir, "BENCHMARK_SUMMARY.json")
	if _, err := os.Stat(summaryPath); os.IsNotExist(err) {
		t.Error("BENCHMARK_SUMMARY.json was not created")
	}
}

func TestOfficialBenchmarks(t *testing.T) {
	// Verify we have the expected benchmarks
	expectedBenchmarks := map[string]bool{
		"mmlu":       true,
		"gsm8k":      true,
		"humaneval":  true,
		"math":       true,
		"hellaswag":  true,
		"arc":        true,
		"truthfulqa": true,
		"bigbench":   true,
	}

	if len(OfficialBenchmarks) != len(expectedBenchmarks) {
		t.Errorf("Expected %d benchmarks, got %d", len(expectedBenchmarks), len(OfficialBenchmarks))
	}

	for _, benchmark := range OfficialBenchmarks {
		if !expectedBenchmarks[benchmark.ID] {
			t.Errorf("Unexpected benchmark: %s", benchmark.ID)
		}

		// Verify all benchmarks have required fields
		if benchmark.Name == "" {
			t.Errorf("Benchmark %s missing name", benchmark.ID)
		}
		if benchmark.Type == "" {
			t.Errorf("Benchmark %s missing type", benchmark.ID)
		}
		if benchmark.LeaderboardURL == "" {
			t.Errorf("Benchmark %s missing leaderboard URL", benchmark.ID)
		}
		if benchmark.Metric == "" {
			t.Errorf("Benchmark %s missing metric", benchmark.ID)
		}
	}
}

func TestSimulateBenchmarkScore(t *testing.T) {
	// Test known benchmarks
	knownBenchmarks := []string{"mmlu", "gsm8k", "humaneval", "math", "hellaswag", "arc", "truthfulqa", "bigbench"}

	for _, benchmarkID := range knownBenchmarks {
		score := simulateBenchmarkScore(benchmarkID)
		if score < 0 || score > 100 {
			t.Errorf("Invalid score for %s: %f", benchmarkID, score)
		}
	}

	// Test unknown benchmark (should return default)
	unknownScore := simulateBenchmarkScore("unknown")
	if unknownScore != 75.0 {
		t.Errorf("Expected default score 75.0, got %f", unknownScore)
	}
}

func TestSaveResults(t *testing.T) {
	tmpDir := filepath.Join(os.TempDir(), "monsterdog_test_save")
	defer os.RemoveAll(tmpDir)

	runner := NewBenchmarkRunner()
	runner.resultsDir = tmpDir

	// Create test results
	results := []BenchmarkResult{
		{
			Name:           "TestBenchmark1",
			Score:          85.5,
			Metric:         "accuracy",
			ExecutionTime:  1.5,
			VSWorldRecord:  "~90%",
			LeaderboardURL: "https://test.com",
		},
		{
			Name:           "TestBenchmark2",
			Score:          90.2,
			Metric:         "pass@1",
			ExecutionTime:  2.3,
			VSWorldRecord:  "~95%",
			LeaderboardURL: "https://test2.com",
		},
	}

	err := runner.saveResults(results)
	if err != nil {
		t.Fatalf("saveResults failed: %v", err)
	}

	// Verify directory was created
	if _, err := os.Stat(tmpDir); os.IsNotExist(err) {
		t.Error("Results directory was not created")
	}

	// Verify summary file exists
	summaryPath := filepath.Join(tmpDir, "BENCHMARK_SUMMARY.json")
	if _, err := os.Stat(summaryPath); os.IsNotExist(err) {
		t.Error("BENCHMARK_SUMMARY.json was not created")
	}

	// Read and verify summary content
	data, err := os.ReadFile(summaryPath)
	if err != nil {
		t.Fatalf("Failed to read summary file: %v", err)
	}

	// Basic validation - should contain expected data
	content := string(data)
	if !containsAll(content, []string{"MONSTERDOG", "V_OMEGA_∞", "TestBenchmark1", "TestBenchmark2"}) {
		t.Error("Summary file missing expected content")
	}
}

func TestBenchmarkResultJSON(t *testing.T) {
	result := BenchmarkResult{
		Name:           "MMLU",
		Score:          85.5,
		Metric:         "accuracy",
		ExecutionTime:  1.234,
		VSWorldRecord:  "~90%",
		LeaderboardURL: "https://example.com",
	}

	if result.Name != "MMLU" {
		t.Errorf("Expected name 'MMLU', got %s", result.Name)
	}
	if result.Score != 85.5 {
		t.Errorf("Expected score 85.5, got %f", result.Score)
	}
	if result.Metric != "accuracy" {
		t.Errorf("Expected metric 'accuracy', got %s", result.Metric)
	}
}

// Helper function
func containsAll(s string, substrs []string) bool {
	for _, substr := range substrs {
		if !contains(s, substr) {
			return false
		}
	}
	return true
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > len(substr) && (s[:len(substr)] == substr || contains(s[1:], substr)))
}
