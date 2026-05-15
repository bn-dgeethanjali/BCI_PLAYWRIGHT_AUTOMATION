# CI/CD Pipeline Setup Guide

## BCI Playwright MCP Automation

This guide covers CI/CD setup for running Playwright MCP tests across different platforms.

---

## Table of Contents

1. [GitHub Actions](#github-actions)
2. [GitLab CI](#gitlab-ci)
3. [Jenkins](#jenkins)
4. [Docker](#docker)
5. [Environment Variables](#environment-variables)
6. [Secrets Configuration](#secrets-configuration)

---

## GitHub Actions

### Files
- `.github/workflows/playwright-mcp-tests.yml` - Main CI pipeline
- `.github/workflows/scheduled-tests.yml` - Nightly/scheduled tests

### Setup Steps

1. **Configure Secrets** (Settings → Secrets → Actions):
   ```
   RULEGENAI_USERNAME=dgeethanjali
   RULEGENAI_PASSWORD=your_password
   RULEGENAI_BASE_URL=http://rule-gen-ai.dev.bci.aws.cudaops.com
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx (optional)
   ```

2. **Enable GitHub Pages** for Allure reports:
   - Go to Settings → Pages
   - Source: Deploy from branch `gh-pages`

3. **Trigger Pipeline**:
   - Automatic: Push to `main` or `develop`
   - Manual: Actions → Playwright MCP Tests → Run workflow

### Commands

```bash
# View workflow runs
gh run list --workflow=playwright-mcp-tests.yml

# Trigger manual run
gh workflow run playwright-mcp-tests.yml -f project=rulegenai -f environment=dev

# Download artifacts
gh run download <run-id> -n test-report-rulegenai
```

---

## GitLab CI

### File
- `.gitlab-ci.yml`

### Setup Steps

1. **Configure Variables** (Settings → CI/CD → Variables):
   ```
   RULEGENAI_USERNAME=dgeethanjali (masked)
   RULEGENAI_PASSWORD=your_password (masked, protected)
   RULEGENAI_BASE_URL=http://rule-gen-ai.dev.bci.aws.cudaops.com
   ```

2. **Enable GitLab Pages**:
   - Allure reports auto-deploy to GitLab Pages

3. **Schedule Pipelines** (CI/CD → Schedules):
   - Create schedule for nightly regression

### Commands

```bash
# Trigger pipeline manually
curl --request POST \
  --header "PRIVATE-TOKEN: <your_token>" \
  "https://gitlab.com/api/v4/projects/<project_id>/pipeline?ref=main"

# View pipeline status
curl --header "PRIVATE-TOKEN: <your_token>" \
  "https://gitlab.com/api/v4/projects/<project_id>/pipelines"
```

---

## Jenkins

### File
- `Jenkinsfile`

### Setup Steps

1. **Install Plugins**:
   - Pipeline
   - Allure Jenkins Plugin
   - HTML Publisher Plugin
   - AnsiColor

2. **Configure Credentials** (Manage Jenkins → Credentials):
   ```
   ID: rulegenai-username
   Type: Secret text
   Value: dgeethanjali

   ID: rulegenai-password
   Type: Secret text
   Value: your_password
   ```

3. **Create Pipeline Job**:
   - New Item → Pipeline
   - Pipeline script from SCM
   - SCM: Git
   - Script Path: Jenkinsfile

4. **Configure Allure**:
   - Manage Jenkins → Global Tool Configuration
   - Add Allure Commandline installation

### Run Pipeline

```bash
# Trigger via CLI
java -jar jenkins-cli.jar -s http://jenkins:8080/ build "BCI-Playwright-MCP" \
  -p PROJECT=rulegenai \
  -p ENVIRONMENT=dev \
  -p TEST_SUITE=all

# Trigger via API
curl -X POST "http://jenkins:8080/job/BCI-Playwright-MCP/buildWithParameters" \
  --user admin:token \
  --data "PROJECT=rulegenai&ENVIRONMENT=dev"
```

---

## Docker

### Files
- `Dockerfile`
- `docker-compose.yml`

### Build & Run

```bash
# Build image
docker build -t bci-playwright-mcp .

# Run all tests
docker run --rm \
  -e RULEGENAI_USERNAME=dgeethanjali \
  -e RULEGENAI_PASSWORD=your_password \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/screenshots:/app/screenshots \
  bci-playwright-mcp

# Run specific test file
docker run --rm \
  -e RULEGENAI_USERNAME=dgeethanjali \
  -e RULEGENAI_PASSWORD=your_password \
  -v $(pwd)/reports:/app/reports \
  bci-playwright-mcp \
  pytest tests/ui/rulegenai/test_login.py -v
```

### Docker Compose

```bash
# Run all RuleGen AI tests
docker-compose up playwright-tests

# Run only login tests
docker-compose --profile login up test-login

# Run only workspace tests
docker-compose --profile workspace up test-workspace

# Run only rule generation tests
docker-compose --profile rule-generation up test-rule-generation

# Start Allure report server
docker-compose --profile report up allure
# View at http://localhost:5050

# Run tests and generate Allure report
docker-compose up playwright-tests
docker-compose --profile report up -d allure

# Clean up
docker-compose down --volumes --rmi local
```

### Using .env file

Create `.env` file:
```env
RULEGENAI_USERNAME=dgeethanjali
RULEGENAI_PASSWORD=Himajabellamkonda@123
RULEGENAI_BASE_URL=http://rule-gen-ai.dev.bci.aws.cudaops.com
MCP_PROJECT=rulegenai
HEADLESS=true
USE_MCP=true
```

Then run:
```bash
docker-compose --env-file .env up playwright-tests
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_MCP` | Enable MCP mode | `true` |
| `MCP_PROJECT` | Project name | `rulegenai` |
| `HEADLESS` | Run headless | `true` |
| `RULEGENAI_USERNAME` | Login username | From config |
| `RULEGENAI_PASSWORD` | Login password | From config |
| `RULEGENAI_BASE_URL` | Application URL | `http://rule-gen-ai.dev.bci.aws.cudaops.com` |
| `TIMEOUT` | Default timeout (ms) | `30000` |
| `SLOW_MO` | Slow down actions (ms) | `0` |

---

## Secrets Configuration

### GitHub Actions Secrets

Go to: Repository → Settings → Secrets and variables → Actions

| Secret Name | Value |
|-------------|-------|
| `RULEGENAI_USERNAME` | `dgeethanjali` |
| `RULEGENAI_PASSWORD` | `your_password` |
| `RULEGENAI_BASE_URL` | `http://rule-gen-ai.dev.bci.aws.cudaops.com` |
| `SLACK_WEBHOOK_URL` | `https://hooks.slack.com/...` (optional) |

### GitLab CI Variables

Go to: Repository → Settings → CI/CD → Variables

| Key | Value | Options |
|-----|-------|---------|
| `RULEGENAI_USERNAME` | `dgeethanjali` | Masked |
| `RULEGENAI_PASSWORD` | `your_password` | Masked, Protected |
| `RULEGENAI_BASE_URL` | `http://...` | - |

### Jenkins Credentials

Go to: Manage Jenkins → Credentials → System → Global credentials

| ID | Type | Description |
|----|------|-------------|
| `rulegenai-username` | Secret text | RuleGen AI username |
| `rulegenai-password` | Secret text | RuleGen AI password |

---

## Quick Reference

### Run Tests Locally
```bash
# Using MCP
USE_MCP=true MCP_PROJECT=rulegenai pytest tests/ui/rulegenai/ -v

# Using Docker
docker-compose up playwright-tests

# Specific test suite
docker-compose --profile login up test-login
```

### View Reports
```bash
# Local HTML report
open reports/rulegenai/report.html

# Allure report (via Docker)
docker-compose --profile report up -d allure
open http://localhost:5050

# GitHub Pages (after CI run)
open https://<username>.github.io/<repo>/
```

### Debug Failed Tests
```bash
# Run with visible browser
HEADLESS=false pytest tests/ui/rulegenai/test_login.py -v

# Run with slow motion
HEADLESS=false SLOW_MO=1000 pytest tests/ui/rulegenai/test_login.py -v

# Capture screenshots on failure
pytest tests/ --screenshot=on --video=on
```

---

## Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CI/CD PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   Push   │───▶│   Lint   │───▶│   Test   │───▶│  Report  │  │
│  │  Code    │    │  Check   │    │   Run    │    │ Generate │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                        │                        │
│                                        ▼                        │
│                              ┌──────────────────┐               │
│                              │  Artifacts       │               │
│                              │  - Screenshots   │               │
│                              │  - HTML Report   │               │
│                              │  - JUnit XML     │               │
│                              │  - Allure Results│               │
│                              └──────────────────┘               │
│                                        │                        │
│                                        ▼                        │
│                              ┌──────────────────┐               │
│                              │    Notify        │               │
│                              │  - Slack         │               │
│                              │  - Email         │               │
│                              │  - GitHub Status │               │
│                              └──────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
