# Dockerfile for BCI Playwright MCP Automation
# Provides consistent test execution environment

FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

LABEL maintainer="BCI QA Team"
LABEL description="BCI Playwright MCP Test Automation Container"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HEADLESS=true \
    USE_MCP=true

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pytest-html pytest-xdist allure-pytest

# Copy project files
COPY . .

# Create directories for artifacts
RUN mkdir -p screenshots reports allure-results

# Default command - run all tests
CMD ["pytest", "tests/ui/rulegenai/", "-v", "--html=reports/report.html", "--self-contained-html"]
