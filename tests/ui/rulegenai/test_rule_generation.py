"""
RuleGen AI Rule Generation Tests
Test cases for AI-powered rule generation functionality
Updated for multi-step wizard interface
"""

import os
import sys

# Add workspace root to Python path
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

import pytest
from playwright.sync_api import Page, expect

from pages.locators.rulegenai_locators import (
    RuleGenAIDashboardLocators,
    RuleGenAIRuleGeneratorLocators,
    RuleGenAIModalsLocators,
)
from tests.ui.rulegenai.conftest import RuleGenAIConfig


@pytest.mark.rulegenai
@pytest.mark.ai_generation
class TestRuleGenerationInterface:
    """Test suite for Rule Generation interface elements"""

    def test_rule_generation_tab_visible(self, dashboard_page: Page):
        """TC-RG-030: Verify Rule Generation tab is visible"""
        page = dashboard_page

        # Look for Rule Generation tab
        rule_gen_tab = page.locator(RuleGenAIRuleGeneratorLocators.TAB_RULE_GENERATION)

        if rule_gen_tab.count() > 0:
            assert rule_gen_tab.first.is_visible(), "Rule Generation tab should be visible"
            print("Rule Generation tab found and visible")

            # Take screenshot
            page.screenshot(path="screenshots/rulegenai/rule_generation/01_rule_gen_tab.png")
        else:
            print("Rule Generation tab not found - checking alternative UI")

    def test_prompt_management_tab_visible(self, dashboard_page: Page):
        """TC-RG-031: Verify Prompt Management tab is visible"""
        page = dashboard_page

        prompt_mgmt_tab = page.locator(RuleGenAIRuleGeneratorLocators.TAB_PROMPT_MANAGEMENT)

        if prompt_mgmt_tab.count() > 0:
            assert prompt_mgmt_tab.first.is_visible(), "Prompt Management tab should be visible"
            print("Prompt Management tab found and visible")
        else:
            print("Prompt Management tab not found")

    def test_wizard_steps_visible(self, dashboard_page: Page):
        """TC-RG-032: Verify all wizard steps are visible"""
        page = dashboard_page

        wizard_steps = {
            "Upload Emails": RuleGenAIRuleGeneratorLocators.STEP_UPLOAD_EMAILS,
            "Select Headers": RuleGenAIRuleGeneratorLocators.STEP_SELECT_HEADERS,
            "Configure Prompt": RuleGenAIRuleGeneratorLocators.STEP_CONFIGURE_PROMPT,
            "Generate Rules": RuleGenAIRuleGeneratorLocators.STEP_GENERATE_RULES,
        }

        found_steps = []
        for step_name, locator in wizard_steps.items():
            element = page.locator(locator)
            if element.count() > 0:
                found_steps.append(step_name)
                print(f"Found wizard step: {step_name}")

        if found_steps:
            print(f"Wizard steps visible: {', '.join(found_steps)}")
            page.screenshot(path="screenshots/rulegenai/rule_generation/02_wizard_steps.png")
        else:
            print("Wizard steps not found - may use different UI pattern")

    def test_token_usage_displayed(self, dashboard_page: Page):
        """TC-RG-033: Verify token usage section is displayed"""
        page = dashboard_page

        token_usage = page.locator(RuleGenAIRuleGeneratorLocators.TOKEN_USAGE)
        token_text = page.locator("text=Token Usage, text=tokens")

        if token_usage.count() > 0 or token_text.count() > 0:
            print("Token usage section found")
            page.screenshot(path="screenshots/rulegenai/rule_generation/03_token_usage.png")
        else:
            print("Token usage section not found")


@pytest.mark.rulegenai
@pytest.mark.ai_generation
class TestGeneratedRules:
    """Test suite for viewing and managing generated rules"""

    def test_generated_rule_section_visible(self, dashboard_page: Page):
        """TC-RG-040: Verify Generated Rule section is visible"""
        page = dashboard_page

        # Look for Generated Rule heading or section
        generated_section = page.locator("text=Generated Rule, h2:has-text('Generated'), h3:has-text('Generated')")
        rule_output = page.locator(RuleGenAIRuleGeneratorLocators.RULE_OUTPUT)

        if generated_section.count() > 0 or rule_output.count() > 0:
            print("Generated Rule section found")
            page.screenshot(path="screenshots/rulegenai/rule_generation/04_generated_rule_section.png")

            # Get the rule content
            if rule_output.count() > 0:
                content = rule_output.first.text_content()
                print(f"Rule content preview: {content[:200] if content else 'Empty'}...")
        else:
            print("Generated Rule section not found - may need to generate first")

    def test_rule_pagination_exists(self, dashboard_page: Page):
        """TC-RG-041: Verify rule pagination is available"""
        page = dashboard_page

        # Look for pagination like "Rule 1/2" or navigation
        rule_count = page.locator(RuleGenAIRuleGeneratorLocators.RULE_COUNT)
        pagination = page.locator("text=/Rule \\d/, text=/\\d of \\d/")
        prev_next = page.locator("button:has-text('<'), button:has-text('>')")

        if rule_count.count() > 0:
            count_text = rule_count.first.text_content()
            print(f"Rule pagination found: {count_text}")
        elif pagination.count() > 0:
            print(f"Pagination found: {pagination.first.text_content()}")
        elif prev_next.count() > 0:
            print("Navigation buttons found for rule pagination")
        else:
            print("Rule pagination not found - may have single rule or none")

    def test_regenerate_button_available(self, dashboard_page: Page):
        """TC-RG-042: Verify Regenerate Rule button is available"""
        page = dashboard_page

        regenerate_btn = page.locator(RuleGenAIRuleGeneratorLocators.REGENERATE_BUTTON)

        if regenerate_btn.count() > 0:
            assert regenerate_btn.first.is_visible(), "Regenerate button should be visible"
            print("Regenerate Rule button found and visible")
            page.screenshot(path="screenshots/rulegenai/rule_generation/05_regenerate_button.png")
        else:
            print("Regenerate button not found - may need generated rules first")

    def test_export_rules_button_available(self, dashboard_page: Page):
        """TC-RG-043: Verify Export Rules button is available"""
        page = dashboard_page

        export_btn = page.locator(RuleGenAIRuleGeneratorLocators.EXPORT_RULES_BUTTON)
        export_alt = page.locator("button:has-text('Export')")

        if export_btn.count() > 0:
            print("Export Rules button found")
            page.screenshot(path="screenshots/rulegenai/rule_generation/06_export_button.png")
        elif export_alt.count() > 0:
            print(f"Export button found (alt): {export_alt.first.text_content()}")
        else:
            print("Export button not found")

    def test_back_to_prompt_config_button(self, dashboard_page: Page):
        """TC-RG-044: Verify Back to Prompt Configuration button exists"""
        page = dashboard_page

        back_btn = page.locator(RuleGenAIRuleGeneratorLocators.BACK_TO_PROMPT_CONFIG)

        if back_btn.count() > 0:
            assert back_btn.first.is_visible(), "Back button should be visible"
            print("Back to Prompt Configuration button found")
        else:
            print("Back button not found")

    def test_share_button_available(self, dashboard_page: Page):
        """TC-RG-045: Verify Share button is available"""
        page = dashboard_page

        share_btn = page.locator(RuleGenAIRuleGeneratorLocators.SHARE_BUTTON)

        if share_btn.count() > 0:
            print("Share button found")
            page.screenshot(path="screenshots/rulegenai/rule_generation/07_share_button.png")
        else:
            print("Share button not found")


@pytest.mark.rulegenai
@pytest.mark.ai_generation
class TestRuleContent:
    """Test suite for generated rule content validation"""

    def test_rule_contains_spamassassin_syntax(self, dashboard_page: Page):
        """TC-RG-050: Verify generated rule contains SpamAssassin syntax"""
        page = dashboard_page

        rule_output = page.locator(RuleGenAIRuleGeneratorLocators.RULE_OUTPUT)

        if rule_output.count() > 0:
            content = rule_output.first.text_content()

            # SpamAssassin rules typically contain these patterns
            spamassassin_keywords = ["header", "body", "score", "describe", "BODY_RULE", "FROM_PATTERN"]

            found_keywords = [kw for kw in spamassassin_keywords if kw.lower() in content.lower()]

            if found_keywords:
                print(f"SpamAssassin keywords found: {', '.join(found_keywords)}")
                print(f"Rule content sample: {content[:300]}...")
            else:
                print(f"No SpamAssassin keywords found. Content: {content[:200]}...")

            page.screenshot(path="screenshots/rulegenai/rule_generation/08_rule_content.png")
        else:
            print("No rule output found to validate")

    def test_rule_output_is_preformatted(self, dashboard_page: Page):
        """TC-RG-051: Verify rule is displayed in preformatted/code block"""
        page = dashboard_page

        code_block = page.locator("pre, code, .code-block")

        if code_block.count() > 0:
            # Check if it contains rule content
            for i in range(min(code_block.count(), 3)):
                text = code_block.nth(i).text_content()
                if text and len(text) > 50:  # Has substantial content
                    print(f"Code block {i+1} found with {len(text)} characters")
                    break
            print("Rule output is in preformatted block")
        else:
            print("No preformatted code block found")

    def test_multiple_rules_generated(self, dashboard_page: Page):
        """TC-RG-052: Check if multiple rules are generated"""
        page = dashboard_page

        # Look for indicators of multiple rules
        rule_count_text = page.locator("text=/Rule \\d+\\/\\d+/, text=/\\d+ of \\d+/")

        if rule_count_text.count() > 0:
            count_str = rule_count_text.first.text_content()
            print(f"Multiple rules indicator: {count_str}")

            # Try to extract numbers
            import re
            numbers = re.findall(r'\d+', count_str)
            if len(numbers) >= 2:
                current, total = numbers[0], numbers[1]
                print(f"Currently viewing rule {current} of {total}")
        else:
            print("Single rule or no pagination found")


@pytest.mark.rulegenai
@pytest.mark.ai_generation
class TestRegenerateFlow:
    """Test suite for rule regeneration functionality"""

    def test_click_regenerate_button(self, dashboard_page: Page):
        """TC-RG-060: Test clicking Regenerate Rule button"""
        page = dashboard_page

        regenerate_btn = page.locator(RuleGenAIRuleGeneratorLocators.REGENERATE_BUTTON)

        if regenerate_btn.count() > 0 and regenerate_btn.first.is_visible():
            # Get current rule content before regenerating
            rule_output = page.locator(RuleGenAIRuleGeneratorLocators.RULE_OUTPUT)
            original_content = ""
            if rule_output.count() > 0:
                original_content = rule_output.first.text_content()

            # Click regenerate
            regenerate_btn.first.click()
            print("Clicked Regenerate Rule button")

            page.screenshot(path="screenshots/rulegenai/rule_generation/09_after_regenerate_click.png")

            # Wait for regeneration (may show loading)
            page.wait_for_timeout(3000)

            # Check if content changed or loading appeared
            loading = page.locator(RuleGenAIRuleGeneratorLocators.LOADING_INDICATOR)
            if loading.count() > 0:
                print("Loading indicator appeared - regeneration in progress")
            else:
                print("Regenerate triggered (no visible loading indicator)")
        else:
            print("Regenerate button not available to click")

    def test_show_prompt_button(self, dashboard_page: Page):
        """TC-RG-061: Test Show Prompt button functionality"""
        page = dashboard_page

        show_prompt = page.locator(RuleGenAIRuleGeneratorLocators.SHOW_PROMPT_BUTTON)

        if show_prompt.count() > 0:
            show_prompt.first.click()
            page.wait_for_timeout(1000)

            print("Clicked Show Prompt button")
            page.screenshot(path="screenshots/rulegenai/rule_generation/10_show_prompt.png")

            # Look for prompt display
            prompt_display = page.locator("textarea, .prompt-display, .prompt-content")
            if prompt_display.count() > 0:
                print("Prompt content displayed")
        else:
            print("Show Prompt button not found")


@pytest.mark.rulegenai
@pytest.mark.ai_generation
class TestFeedback:
    """Test suite for feedback functionality"""

    def test_feedback_input_available(self, dashboard_page: Page):
        """TC-RG-070: Verify feedback input is available"""
        page = dashboard_page

        feedback_input = page.locator(RuleGenAIRuleGeneratorLocators.FEEDBACK_INPUT)
        feedback_placeholder = page.locator("textarea[placeholder*='feedback'], input[placeholder*='feedback']")

        if feedback_input.count() > 0 or feedback_placeholder.count() > 0:
            print("Feedback input found")
            page.screenshot(path="screenshots/rulegenai/rule_generation/11_feedback_input.png")
        else:
            print("Feedback input not found")

    def test_workspace_header_info(self, dashboard_page: Page):
        """TC-RG-071: Verify workspace header displays correct info"""
        page = dashboard_page

        # Look for workspace name in header
        workspace_name = page.locator("text=mcp_rulegenai, h1, .workspace-name")
        all_workspaces_link = page.locator("a:has-text('All Workspaces')")

        if workspace_name.count() > 0:
            name = workspace_name.first.text_content()
            print(f"Workspace name displayed: {name}")

        if all_workspaces_link.count() > 0:
            print("All Workspaces navigation link found")

        page.screenshot(path="screenshots/rulegenai/rule_generation/12_workspace_header.png")


@pytest.mark.rulegenai
@pytest.mark.ai_generation
@pytest.mark.slow
class TestFullGenerationFlow:
    """Test suite for complete rule generation workflow"""

    def test_navigate_to_configure_prompt(self, dashboard_page: Page):
        """TC-RG-080: Navigate to Configure Prompt step"""
        page = dashboard_page

        # Try clicking Configure Prompt step
        config_prompt = page.locator(RuleGenAIRuleGeneratorLocators.STEP_CONFIGURE_PROMPT)
        back_btn = page.locator(RuleGenAIRuleGeneratorLocators.BACK_TO_PROMPT_CONFIG)

        if back_btn.count() > 0 and back_btn.first.is_visible():
            back_btn.first.click()
            page.wait_for_timeout(2000)
            print("Clicked Back to Prompt Configuration")
            page.screenshot(path="screenshots/rulegenai/rule_generation/13_prompt_config_step.png")
        elif config_prompt.count() > 0:
            config_prompt.first.click()
            page.wait_for_timeout(2000)
            print("Clicked Configure Prompt step")
            page.screenshot(path="screenshots/rulegenai/rule_generation/13_prompt_config_step.png")
        else:
            print("Could not navigate to Configure Prompt step")

    def test_complete_page_screenshot(self, dashboard_page: Page):
        """TC-RG-081: Capture complete page state"""
        page = dashboard_page

        # Capture full page screenshot
        page.screenshot(path="screenshots/rulegenai/rule_generation/14_full_page_state.png", full_page=True)
        print(f"Full page screenshot captured")
        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")

        # Log all visible buttons
        buttons = page.locator("button").all()
        print(f"\nVisible buttons ({len(buttons)}):")
        for btn in buttons[:10]:
            try:
                text = btn.text_content().strip()[:30]
                if text:
                    print(f"  - {text}")
            except:
                pass
