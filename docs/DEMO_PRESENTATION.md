# 30-Minute Demo: Building Test Automation with Playwright MCP + AI

## BCI Playwright Automation Framework

**Duration:** 30 Minutes  
**Audience:** QA Engineers, Developers, Tech Leads  
**Tools Used:** Playwright, MCP (Model Context Protocol), Claude AI

---

## Demo Agenda

| Time | Section | Duration |
|------|---------|----------|
| 0:00 | Introduction & Problem Statement | 3 min |
| 3:00 | Traditional vs AI-Assisted Approach | 5 min |
| 8:00 | Live Demo: Framework Architecture | 5 min |
| 13:00 | Live Demo: AI Locator Discovery | 7 min |
| 20:00 | Live Demo: Test Execution | 5 min |
| 25:00 | CI/CD Integration | 3 min |
| 28:00 | Q&A | 2 min |

---

## Section 1: Introduction & Problem Statement (3 min)

### Slide 1: The Challenge

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE TESTING CHALLENGE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ❌ Manual test writing is TIME-CONSUMING                      │
│   ❌ UI changes BREAK tests frequently                          │
│   ❌ Finding correct LOCATORS is tedious                        │
│   ❌ Multiple projects need SEPARATE frameworks                 │
│   ❌ Debugging failures requires MANUAL investigation           │
│                                                                 │
│   QUESTION: Can AI help solve these problems?                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Talking Points:
- "Today I'll show you how we built a test automation framework using AI assistance"
- "We'll see how Claude AI helped us discover locators, diagnose failures, and generate test code"
- "The framework supports multiple projects through configuration, not code duplication"

---

## Section 2: Traditional vs AI-Assisted Approach (5 min)

### Slide 2: Traditional Workflow

```
TRADITIONAL TEST AUTOMATION WORKFLOW
═══════════════════════════════════════════════════════════════

Step 1: Manually inspect page (DevTools)          ⏱️ 15 min
Step 2: Write locators                            ⏱️ 20 min  
Step 3: Write test code                           ⏱️ 30 min
Step 4: Run test → FAILS                          ⏱️ 5 min
Step 5: Debug (wrong locator)                     ⏱️ 20 min
Step 6: Fix and re-run                            ⏱️ 10 min
Step 7: Test passes                               ⏱️ —
                                          ─────────────────
                                          TOTAL: ~100 min
```

### Slide 3: AI-Assisted Workflow

```
AI-ASSISTED TEST AUTOMATION WORKFLOW
═══════════════════════════════════════════════════════════════

Step 1: Ask AI to analyze the page                ⏱️ 2 min
        → AI inspects, finds locators automatically

Step 2: AI generates test code                    ⏱️ 3 min
        → Based on actual page structure

Step 3: Run test → PASSES (or AI diagnoses)       ⏱️ 5 min
        → AI fixes issues if test fails
                                          ─────────────────
                                          TOTAL: ~10 min

                    ⚡ 10x FASTER ⚡
```

### Live Demo: Show the actual conversation

```
USER: "Create test cases for RuleGen AI dashboard at 
       http://rule-gen-ai.dev.bci.aws.cudaops.com/workspaces/12"

AI: "I'll analyze the page structure first..."
    [AI navigates, takes screenshots, discovers UI elements]
    
    "Found: Multi-step wizard interface with:
     - Rule Generation tab
     - Prompt Management tab  
     - 4 wizard steps
     - Generated Rule section"
    
    [AI creates appropriate locators and tests]
```

---

## Section 3: Framework Architecture (5 min)

### Slide 4: Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│              BCI PLAYWRIGHT MCP ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   Tests     │     │   Pages     │     │    MCP      │       │
│  │             │     │             │     │   Layer     │       │
│  │ test_login  │     │  locators/  │     │             │       │
│  │ test_rules  │────▶│  rulegenai  │────▶│ mcp_config  │       │
│  │ test_work   │     │  _locators  │     │ mcp_fixtures│       │
│  └─────────────┘     └─────────────┘     └──────┬──────┘       │
│                                                  │              │
│                                          ┌───────▼───────┐      │
│                                          │  YAML Config  │      │
│                                          │               │      │
│                                          │ rulegenai.yaml│      │
│                                          │ mailxray.yaml │      │
│                                          └───────────────┘      │
│                                                                 │
│  🤖 AI ROLE: Designed architecture, created all components      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Live Demo: Show project structure

```bash
# Show the structure AI created
tree -L 3 --dirsfirst

BCI_PLAYWRIGHT_AUTOMATION_MCP/
├── mcp/
│   ├── projects/
│   │   └── rulegenai.yaml      # AI created config
│   ├── mcp_config.py           # AI created
│   ├── mcp_fixtures.py         # AI created
│   └── mcp_browser_adapter.py  # AI created
├── pages/
│   └── locators/
│       └── rulegenai_locators.py  # AI discovered locators
├── tests/
│   └── ui/
│       └── rulegenai/
│           ├── test_login.py          # AI created
│           ├── test_workspace.py      # AI created
│           ├── test_rule_generation.py # AI created
│           └── conftest.py            # AI created
└── docs/
    └── CI_CD_SETUP.md          # AI created
```

### Talking Point:
- "Every file you see here was created or modified by AI"
- "I provided the requirements, AI designed the architecture"

---

## Section 4: AI Locator Discovery (7 min) ⭐ KEY DEMO

### Slide 5: The Problem - Wrong Locators

```
ORIGINAL ASSUMPTION (Human guess):
══════════════════════════════════════════════════

# We assumed a simple login form
class LoginLocators:
    USERNAME = "input[name='email']"      # ❌ WRONG
    PASSWORD = "input[name='password']"   # ❌ WRONG  
    LOGIN_BTN = "button:has-text('Login')" # ❌ WRONG

TEST RESULT: ❌ FAILED - Element not found
```

### Live Demo: AI Diagnosis

```python
# AI analyzes the actual page
"""
AI DIAGNOSTIC OUTPUT:
═══════════════════════════════════════════════════════════════

[1] Navigating to login page...
    URL: http://rule-gen-ai.dev.bci.aws.cudaops.com/login/

[2] Scanning for form elements...
    ✓ Found: <input id="username" name="username">
    ✓ Found: <input type="password" id="password">
    ✓ Found: <button type="submit">Sign in</button>

[3] CORRECT LOCATORS:
    USERNAME = "#username, input[name='username']"
    PASSWORD = "#password, input[type='password']"  
    LOGIN_BTN = "button[type='submit'], button:has-text('Sign in')"

[4] Additional elements discovered:
    - Remember me checkbox
    - "All Workspaces" navigation link
    - User menu dropdown
"""
```

### Live Demo: Complex UI Discovery

```python
# AI discovered the RuleGen AI is a MULTI-STEP WIZARD
"""
AI DIAGNOSTIC OUTPUT:
═══════════════════════════════════════════════════════════════

❌ ORIGINAL ASSUMPTION: Simple form with prompt input
   PROMPT_INPUT = "textarea#prompt"
   GENERATE_BTN = "button:has-text('Generate')"

✅ ACTUAL UI STRUCTURE (AI discovered):
   
   ┌─────────────────────────────────────────────────┐
   │  [Rule Generation]  [Prompt Management]  ← TABS │
   ├─────────────────────────────────────────────────┤
   │                                                 │
   │  WIZARD STEPS:                                  │
   │  ① Upload Emails                                │
   │  ② Select Headers                               │
   │  ③ Configure Prompt  ← Prompt input is HERE    │
   │  ④ Generate Rules                               │
   │                                                 │
   │  ┌─────────────────────────────────────────┐   │
   │  │ Generated Rule                          │   │
   │  │ Rule 1/2                                │   │
   │  │ [Regenerate Rule] [Export Rules]        │   │
   │  └─────────────────────────────────────────┘   │
   │                                                 │
   │  [Back to Prompt Configuration] [Generating...] │
   └─────────────────────────────────────────────────┘

CORRECTED LOCATORS (by AI):
   TAB_RULE_GENERATION = "button:has-text('Rule Generation')"
   TAB_PROMPT_MANAGEMENT = "button:has-text('Prompt Management')"
   STEP_CONFIGURE_PROMPT = "button:has-text('Configure Prompt')"
   REGENERATE_BUTTON = "button:has-text('Regenerate Rule')"
   EXPORT_RULES_BUTTON = "button:has-text('Export Rules')"
"""
```

### Show Actual Code Diff

```diff
# Before AI (FAILED)
- PROMPT_INPUT = "textarea#prompt"
- GENERATE_BUTTON = "button:has-text('Generate')"

# After AI Analysis (WORKS)
+ TAB_RULE_GENERATION = "button:has-text('Rule Generation')"
+ STEP_UPLOAD_EMAILS = "button:has-text('Upload Emails')"
+ STEP_SELECT_HEADERS = "button:has-text('Select Headers')"
+ STEP_CONFIGURE_PROMPT = "button:has-text('Configure Prompt')"
+ STEP_GENERATE_RULES = "button:has-text('Generate Rules')"
+ REGENERATE_BUTTON = "button:has-text('Regenerate Rule')"
+ EXPORT_RULES_BUTTON = "button:has-text('Export Rules')"
```

---

## Section 5: Test Execution Demo (5 min)

### Live Demo: Run Tests

```bash
# Terminal 1: Run tests with MCP
cd /Users/dgeethanjali/Documents/BCI_PLAYWRIGHT_AUTOMATION_MCP

# Single command - credentials from config
source .venv/bin/activate && \
USE_MCP=true MCP_PROJECT=rulegenai HEADLESS=true \
pytest tests/ui/rulegenai/test_rule_generation.py -v
```

### Show Results

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2

tests/ui/rulegenai/test_rule_generation.py::TestRuleGenerationInterface::test_rule_generation_tab_visible PASSED
tests/ui/rulegenai/test_rule_generation.py::TestRuleGenerationInterface::test_prompt_management_tab_visible PASSED
tests/ui/rulegenai/test_rule_generation.py::TestRuleGenerationInterface::test_wizard_steps_visible PASSED
tests/ui/rulegenai/test_rule_generation.py::TestGeneratedRules::test_generated_rule_section_visible PASSED
tests/ui/rulegenai/test_rule_generation.py::TestGeneratedRules::test_regenerate_button_available PASSED
...

======================== 19 passed in 224.42s (0:03:44) ========================
```

### Show Screenshots Generated

```bash
# AI created tests that capture screenshots at key points
ls screenshots/rulegenai/

01_login_page.png
02_after_login.png
03_workspace_12.png
04_rule_generation_tab.png
05_generated_rule_section.png
...
```

---

## Section 6: AI Role Summary (2 min)

### Slide 6: What AI Did

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI CONTRIBUTION SUMMARY                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  ARCHITECTURE DESIGN                                        │
│      → Designed MCP adapter layer pattern                       │
│      → Created config-driven multi-project structure            │
│      → Built reusable fixtures and utilities                    │
│                                                                 │
│  2️⃣  LOCATOR DISCOVERY                                          │
│      → Analyzed actual page structure                           │
│      → Found correct selectors automatically                    │
│      → Discovered multi-step wizard (not simple form)           │
│                                                                 │
│  3️⃣  TEST GENERATION                                            │
│      → Created 40+ test cases across 4 test files               │
│      → Added proper assertions and error handling               │
│      → Included screenshot capture at key points                │
│                                                                 │
│  4️⃣  FAILURE DIAGNOSIS                                          │
│      → Identified why tests were failing                        │
│      → Fixed timeout issues                                     │
│      → Resolved session state problems                          │
│                                                                 │
│  5️⃣  CI/CD SETUP                                                │
│      → Created GitHub Actions workflows                         │
│      → Created GitLab CI pipeline                               │
│      → Created Jenkins pipeline                                 │
│      → Created Docker configuration                             │
│                                                                 │
│  ⏱️  TIME SAVED: ~20+ hours of manual work                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 7: CI/CD Integration (3 min)

### Slide 7: Pipeline Created by AI

```yaml
# .github/workflows/playwright-mcp-tests.yml (AI Created)

name: Playwright MCP Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Install Playwright
        run: playwright install chromium
      - name: Run Tests
        env:
          USE_MCP: true
          MCP_PROJECT: rulegenai
        run: pytest tests/ui/rulegenai/ -v --html=reports/report.html
```

### Show Multiple Platforms

```
AI created CI/CD for ALL major platforms:

├── .github/workflows/
│   ├── playwright-mcp-tests.yml    # GitHub Actions
│   └── scheduled-tests.yml         # Nightly runs
├── .gitlab-ci.yml                  # GitLab CI
├── Jenkinsfile                     # Jenkins
├── Dockerfile                      # Container
└── docker-compose.yml              # Docker Compose
```

---

## Section 8: Key Takeaways (1 min)

### Slide 8: Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                      KEY TAKEAWAYS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ AI can ANALYZE pages and find correct locators              │
│                                                                 │
│  ✅ AI can DIAGNOSE test failures and suggest fixes             │
│                                                                 │
│  ✅ AI can GENERATE complete test suites                        │
│                                                                 │
│  ✅ AI can CREATE CI/CD pipelines for multiple platforms        │
│                                                                 │
│  ✅ Configuration-driven approach enables MULTI-PROJECT support │
│                                                                 │
│  ⚡ 10x FASTER than traditional manual approach                 │
│                                                                 │
│  🎯 Same Playwright code - AI just helps you write it faster   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Demo Commands Quick Reference

```bash
# 1. Show project structure
cd /Users/dgeethanjali/Documents/BCI_PLAYWRIGHT_AUTOMATION_MCP
tree -L 3 --dirsfirst

# 2. Show config file
cat mcp/projects/rulegenai.yaml

# 3. Show locators discovered by AI
cat pages/locators/rulegenai_locators.py

# 4. Run login tests
source .venv/bin/activate
USE_MCP=true MCP_PROJECT=rulegenai pytest tests/ui/rulegenai/test_login.py -v

# 5. Run all tests
USE_MCP=true MCP_PROJECT=rulegenai pytest tests/ui/rulegenai/ -v

# 6. Show screenshots
open screenshots/rulegenai/

# 7. Run with visible browser (for demo)
HEADLESS=false USE_MCP=true MCP_PROJECT=rulegenai pytest tests/ui/rulegenai/test_login.py -v

# 8. Docker run
docker-compose up playwright-tests
```

---

## Q&A Preparation

### Expected Questions:

**Q: Does AI write the actual test code?**
A: Yes, AI generates complete Python/Playwright code. You can modify it as needed.

**Q: What if the UI changes?**
A: Run AI diagnosis again - it will find new locators and update tests.

**Q: Is the test code different from normal Playwright?**
A: No, it's standard Playwright API. AI just helps write it faster.

**Q: Can we use this for other projects?**
A: Yes! Just create a new YAML config file and set `MCP_PROJECT=yourproject`.

**Q: What about test maintenance?**
A: AI can diagnose failures and suggest fixes, reducing maintenance time.

---

## Files to Open During Demo

1. `mcp/projects/rulegenai.yaml` - Show configuration
2. `pages/locators/rulegenai_locators.py` - Show AI-discovered locators
3. `tests/ui/rulegenai/test_rule_generation.py` - Show AI-generated tests
4. `screenshots/rulegenai/diagnostic/GENERATOR_FOUND.png` - Show AI screenshot
5. `.github/workflows/playwright-mcp-tests.yml` - Show CI/CD

---

## Demo Checklist

- [ ] Virtual environment activated
- [ ] Test credentials configured in config
- [ ] Browser installed (`playwright install chromium`)
- [ ] Screenshots directory exists
- [ ] Terminal ready with commands
- [ ] IDE open with key files
- [ ] Network connectivity to test application
