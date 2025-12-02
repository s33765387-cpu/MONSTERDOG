# MONSTERDOG Makefile
# Build and test automation for Go implementation

.PHONY: all build test clean run benchmark install lint help

# Build variables
BINARY_NAME=monsterdog
BUILD_DIR=build
MAIN_PATH=./cmd/monsterdog

# Go variables
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
GOMOD=$(GOCMD) mod
GOFMT=$(GOCMD) fmt

# Default target
all: clean build test

## help: Display this help message
help:
	@echo "MONSTERDOG - Makefile Commands"
	@echo "==============================="
	@echo ""
	@echo "Available targets:"
	@echo "  make build      - Build the MONSTERDOG binary"
	@echo "  make test       - Run all tests"
	@echo "  make run        - Build and run MONSTERDOG"
	@echo "  make benchmark  - Run with benchmarks enabled"
	@echo "  make fulltrutl  - Run in FULLTRUTL mode"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make install    - Install dependencies"
	@echo "  make lint       - Run code linters"
	@echo "  make fmt        - Format Go code"
	@echo "  make help       - Display this help message"
	@echo ""

## build: Build the MONSTERDOG binary
build:
	@echo "🔨 Building MONSTERDOG..."
	@mkdir -p $(BUILD_DIR)
	$(GOBUILD) -o $(BUILD_DIR)/$(BINARY_NAME) -v $(MAIN_PATH)
	@echo "✅ Build complete: $(BUILD_DIR)/$(BINARY_NAME)"

## test: Run all tests
test:
	@echo "🧪 Running tests..."
	$(GOTEST) -v ./...
	@echo "✅ Tests complete"

## test-coverage: Run tests with coverage
test-coverage:
	@echo "🧪 Running tests with coverage..."
	$(GOTEST) -v -coverprofile=coverage.out ./...
	$(GOCMD) tool cover -html=coverage.out -o coverage.html
	@echo "✅ Coverage report generated: coverage.html"

## run: Build and run MONSTERDOG
run: build
	@echo "🚀 Running MONSTERDOG..."
	./$(BUILD_DIR)/$(BINARY_NAME)

## benchmark: Run MONSTERDOG with benchmarks
benchmark: build
	@echo "🏆 Running MONSTERDOG with benchmarks..."
	MONSTERDOG_BENCHMARK=true ./$(BUILD_DIR)/$(BINARY_NAME)

## fulltrutl: Run MONSTERDOG in FULLTRUTL mode
fulltrutl: build
	@echo "⚡️ Running MONSTERDOG in FULLTRUTL mode..."
	MONSTERDOG_MODE=FULLTRUTL ./$(BUILD_DIR)/$(BINARY_NAME)

## fulltrutl-benchmark: Run MONSTERDOG in FULLTRUTL mode with benchmarks
fulltrutl-benchmark: build
	@echo "⚡️ Running MONSTERDOG in FULLTRUTL mode with benchmarks..."
	MONSTERDOG_MODE=FULLTRUTL MONSTERDOG_BENCHMARK=true ./$(BUILD_DIR)/$(BINARY_NAME)

## clean: Clean build artifacts
clean:
	@echo "🧹 Cleaning..."
	$(GOCLEAN)
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html
	@echo "✅ Clean complete"

## install: Install dependencies
install:
	@echo "📦 Installing dependencies..."
	$(GOMOD) download
	$(GOMOD) tidy
	@echo "✅ Dependencies installed"

## lint: Run linters (requires golangci-lint)
lint:
	@echo "🔍 Running linters..."
	@if command -v golangci-lint >/dev/null 2>&1; then \
		golangci-lint run ./...; \
	else \
		echo "⚠️  golangci-lint not installed. Run: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest"; \
	fi

## fmt: Format Go code
fmt:
	@echo "✨ Formatting code..."
	$(GOFMT) ./...
	@echo "✅ Code formatted"

## vet: Run go vet
vet:
	@echo "🔍 Running go vet..."
	$(GOCMD) vet ./...
	@echo "✅ Vet complete"

## mod-verify: Verify dependencies
mod-verify:
	@echo "🔍 Verifying dependencies..."
	$(GOMOD) verify
	@echo "✅ Dependencies verified"

## docker-build: Build Docker image (if Dockerfile exists)
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t monsterdog:latest .

## version: Display Go version
version:
	@$(GOCMD) version

.DEFAULT_GOAL := help
