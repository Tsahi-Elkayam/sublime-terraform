# Makefile for Terraform Sublime Text Plugin

.PHONY: help install test test-unit test-integration test-performance test-all lint format clean build release

PYTHON := python3
PIP := pip3
PACKAGE_NAME := Terraform
TEST_DIR := tests
BUILD_DIR := build
RELEASE_DIR := release

# Default target
help:
	@echo "Terraform Sublime Text Plugin - Available targets:"
	@echo ""
	@echo "  install          Install development dependencies"
	@echo "  test             Run unit tests"
	@echo "  test-unit        Run unit tests with coverage"
	@echo "  test-integration Run integration tests"
	@echo "  test-performance Run performance tests"
	@echo "  test-all         Run all tests"
	@echo "  lint             Run code linters"
	@echo "  format           Format code with black and isort"
	@echo "  clean            Clean build artifacts"
	@echo "  build            Build plugin package"
	@echo "  release          Create release package"
	@echo ""

# Install dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-test.txt
	@echo "✓ Dependencies installed"

# Run unit tests
test:
	cd $(TEST_DIR) && $(PYTHON) run_tests.py -v

# Run unit tests with coverage
test-unit:
	cd $(TEST_DIR) && coverage run -m pytest -v --tb=short
	cd $(TEST_DIR) && coverage report
	cd $(TEST_DIR) && coverage html
	@echo "✓ Coverage report generated in $(TEST_DIR)/htmlcov/"

# Run integration tests
test-integration:
	cd $(TEST_DIR) && $(PYTHON) run_tests.py --integration -v

# Run performance tests
test-performance:
	cd $(TEST_DIR) && $(PYTHON) run_tests.py --performance -v

# Run all tests
test-all:
	cd $(TEST_DIR) && $(PYTHON) run_tests.py -v
	cd $(TEST_DIR) && $(PYTHON) run_tests.py --integration -v
	cd $(TEST_DIR) && $(PYTHON) run_tests.py --performance -v

# Run linters
lint:
	flake8 $(PACKAGE_NAME) --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 $(PACKAGE_NAME) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	mypy $(PACKAGE_NAME) --ignore-missing-imports
	@echo "✓ Linting complete"

# Format code
format:
	black $(PACKAGE_NAME)
	isort $(PACKAGE_NAME)
	@echo "✓ Code formatted"

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(RELEASE_DIR)
	rm -rf $(TEST_DIR)/htmlcov
	rm -rf $(TEST_DIR)/.coverage
	rm -rf $(TEST_DIR)/__pycache__
	rm -rf $(PACKAGE_NAME)/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "✓ Cleaned build artifacts"

# Build plugin
build: clean
	@echo "Building $(PACKAGE_NAME) plugin..."
	mkdir -p $(BUILD_DIR)
	
	# Copy plugin files
	cp -r *.py $(BUILD_DIR)/
	cp -r syntaxes $(BUILD_DIR)/
	cp -r messages $(BUILD_DIR)/
	cp *.sublime-* $(BUILD_DIR)/
	cp *.json $(BUILD_DIR)/
	cp README.md $(BUILD_DIR)/
	cp LICENSE $(BUILD_DIR)/
	
	# Remove test files
	rm -rf $(BUILD_DIR)/test_*
	rm -rf $(BUILD_DIR)/*test*.py
	
	@echo "✓ Build complete in $(BUILD_DIR)/"

# Create release package
release: build
	@echo "Creating release package..."
	mkdir -p $(RELEASE_DIR)
	
	# Create .sublime-package (zip file)
	cd $(BUILD_DIR) && zip -r ../$(RELEASE_DIR)/$(PACKAGE_NAME).sublime-package *
	
	# Create source archive
	git archive --format=zip --prefix=$(PACKAGE_NAME)/ HEAD > $(RELEASE_DIR)/$(PACKAGE_NAME)-source.zip
	
	# Generate checksums
	cd $(RELEASE_DIR) && sha256sum *.sublime-package *.zip > checksums.txt
	
	@echo "✓ Release package created in $(RELEASE_DIR)/"
	@echo ""
	@ls -la $(RELEASE_DIR)/

# Development helpers
.PHONY: dev watch debug

# Run in development mode
dev:
	cd $(TEST_DIR) && $(PYTHON) -m pytest -v -s --tb=short

# Watch for changes and re-run tests
watch:
	cd $(TEST_DIR) && $(PYTHON) -m pytest-watch -v

# Run with debugging enabled
debug:
	cd $(TEST_DIR) && $(PYTHON) -m pytest -v -s --pdb

# CI/CD helpers
.PHONY: ci-test ci-lint ci-build

# Run tests for CI
ci-test:
	cd $(TEST_DIR) && $(PYTHON) run_tests.py -v --json-report test-results.json --html-report test-results.html

# Run linting for CI
ci-lint:
	flake8 $(PACKAGE_NAME) --format=json --output-file=flake8-report.json || true
	mypy $(PACKAGE_NAME) --html-report mypy-report || true

# Build for CI
ci-build: test-all lint build
	@echo "✓ CI build complete"