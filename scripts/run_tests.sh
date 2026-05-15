#!/bin/bash

# ============================================
# BCI Playwright MCP Test Runner Script
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
PROJECT="${MCP_PROJECT:-rulegenai}"
TEST_SUITE="${TEST_SUITE:-all}"
HEADLESS="${HEADLESS:-true}"
USE_MCP="${USE_MCP:-true}"
REPORT_DIR="reports/${PROJECT}"
SCREENSHOT_DIR="screenshots/${PROJECT}"

# Print banner
echo -e "${BLUE}"
echo "============================================"
echo "  BCI Playwright MCP Test Runner"
echo "============================================"
echo -e "${NC}"

# Show usage
usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -p, --project     Project name (default: rulegenai)"
    echo "  -t, --test        Test suite: all, login, workspace, rule_generation"
    echo "  -h, --headless    Run headless (default: true)"
    echo "  -v, --visible     Run with visible browser"
    echo "  -d, --docker      Run in Docker container"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                          # Run all tests"
    echo "  $0 -t login                 # Run login tests only"
    echo "  $0 -t workspace -v          # Run workspace tests with visible browser"
    echo "  $0 -d                       # Run in Docker"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--project)
            PROJECT="$2"
            shift 2
            ;;
        -t|--test)
            TEST_SUITE="$2"
            shift 2
            ;;
        -h|--headless)
            HEADLESS="true"
            shift
            ;;
        -v|--visible)
            HEADLESS="false"
            shift
            ;;
        -d|--docker)
            USE_DOCKER="true"
            shift
            ;;
        --help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Determine test path
if [ "$TEST_SUITE" == "all" ]; then
    TEST_PATH="tests/ui/${PROJECT}/"
else
    TEST_PATH="tests/ui/${PROJECT}/test_${TEST_SUITE}.py"
fi

# Create directories
mkdir -p "$REPORT_DIR" "$SCREENSHOT_DIR" "allure-results"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Project:     $PROJECT"
echo "  Test Suite:  $TEST_SUITE"
echo "  Test Path:   $TEST_PATH"
echo "  Headless:    $HEADLESS"
echo "  Use MCP:     $USE_MCP"
echo ""

# Run tests
if [ "$USE_DOCKER" == "true" ]; then
    echo -e "${BLUE}Running tests in Docker...${NC}"

    docker-compose run --rm \
        -e MCP_PROJECT="$PROJECT" \
        -e HEADLESS="$HEADLESS" \
        playwright-tests \
        pytest "$TEST_PATH" \
            -v \
            --tb=short \
            --html="reports/${PROJECT}/report.html" \
            --self-contained-html \
            --junitxml="reports/${PROJECT}/junit.xml" \
            --alluredir=allure-results
else
    echo -e "${BLUE}Running tests locally...${NC}"

    # Activate virtual environment if exists
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi

    # Run pytest
    USE_MCP="$USE_MCP" \
    MCP_PROJECT="$PROJECT" \
    HEADLESS="$HEADLESS" \
    pytest "$TEST_PATH" \
        -v \
        --tb=short \
        --html="${REPORT_DIR}/report.html" \
        --self-contained-html \
        --junitxml="${REPORT_DIR}/junit.xml" \
        --alluredir=allure-results
fi

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  ✅ Tests completed successfully!${NC}"
    echo -e "${GREEN}============================================${NC}"
else
    echo ""
    echo -e "${RED}============================================${NC}"
    echo -e "${RED}  ❌ Some tests failed!${NC}"
    echo -e "${RED}============================================${NC}"
fi

echo ""
echo -e "${YELLOW}Reports:${NC}"
echo "  HTML Report:  ${REPORT_DIR}/report.html"
echo "  JUnit XML:    ${REPORT_DIR}/junit.xml"
echo "  Screenshots:  ${SCREENSHOT_DIR}/"
echo "  Allure:       allure-results/"
echo ""
echo -e "${YELLOW}To view Allure report:${NC}"
echo "  allure serve allure-results"
