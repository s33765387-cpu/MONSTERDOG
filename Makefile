# MONSTERDOG Makefile
# Signature: 0x5F3759DF-s33765387-FULLTRUTL-Δ-Ω

.PHONY: all build test clean run help

# Variables
BINARY_NAME=monsterdog
GO=go
GOFLAGS=

all: test build

# Build the application
build:
	@echo "Building $(BINARY_NAME)..."
	$(GO) build $(GOFLAGS) -o $(BINARY_NAME) monsterdog.go
	@echo "Build complete: ./$(BINARY_NAME)"

# Run tests
test:
	@echo "Running tests..."
	$(GO) test -v -cover

# Run tests with race detector
test-race:
	@echo "Running tests with race detector..."
	$(GO) test -v -race

# Run the application
run:
	@echo "Running $(BINARY_NAME)..."
	$(GO) run monsterdog.go

# Run with custom cycle count (example: make run-cycles CYCLES=50)
run-cycles:
	@echo "Running $(BINARY_NAME) with custom cycles..."
	$(GO) run monsterdog.go

# Clean build artifacts
clean:
	@echo "Cleaning..."
	rm -f $(BINARY_NAME)
	$(GO) clean
	@echo "Clean complete"

# Format code
fmt:
	@echo "Formatting code..."
	$(GO) fmt ./...

# Run go vet
vet:
	@echo "Running go vet..."
	$(GO) vet ./...

# Run all checks (format, vet, test)
check: fmt vet test
	@echo "All checks passed!"

# Show help
help:
	@echo "MONSTERDOG V_FINALITY_Ω - Makefile Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  make build      - Build the application"
	@echo "  make test       - Run tests with coverage"
	@echo "  make test-race  - Run tests with race detector"
	@echo "  make run        - Run the application"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make fmt        - Format code"
	@echo "  make vet        - Run go vet"
	@echo "  make check      - Run all checks (fmt, vet, test)"
	@echo "  make help       - Show this help"
	@echo ""
	@echo "Signature: 0x5F3759DF-s33765387-FULLTRUTL-Δ-Ω"
