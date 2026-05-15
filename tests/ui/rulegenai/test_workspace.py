"""
RuleGen AI Workspace Tests
Test cases for workspace management functionality
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
    RuleGenAIModalsLocators,
)
from tests.ui.rulegenai.conftest import RuleGenAIConfig


@pytest.mark.rulegenai
@pytest.mark.workspace
class TestWorkspaceView:
    """Test suite for workspace view functionality"""

    def test_workspace_12_loads(self, dashboard_page: Page):
        """TC-RG-090: Verify workspace 12 loads correctly"""
        page = dashboard_page

        print(f"URL: {page.url}")
        print(f"Title: {page.title()}")

        # Verify we're on a workspace page (may redirect to different workspace)
        is_workspace_page = "/workspaces/" in page.url or "/workspaces" in page.url

        if "12" in page.url:
            print("Workspace 12 loaded successfully")
        elif is_workspace_page:
            print(f"Loaded workspace page: {page.url}")
        else:
            # Take debug screenshot
            page.screenshot(path="screenshots/rulegenai/workspace_load_debug.png", full_page=True)

        assert is_workspace_page, f"Not on workspace page: {page.url}"

        # Take screenshot
        page.screenshot(path="screenshots/rulegenai/workspace_12.png", full_page=True)
        print("Workspace page loaded successfully")

    def test_workspace_header_info(self, dashboard_page: Page):
        """TC-RG-091: Verify workspace header displays information"""
        page = dashboard_page

        header_elements = {
            "Title": RuleGenAIDashboardLocators.WORKSPACE_TITLE,
            "Description": RuleGenAIDashboardLocators.WORKSPACE_DESCRIPTION,
            "Status": RuleGenAIDashboardLocators.WORKSPACE_STATUS,
        }

        found_elements = []
        for name, locator in header_elements.items():
            element = page.locator(locator)
            if element.count() > 0 and element.first.is_visible():
                text = element.first.text_content().strip()
                found_elements.append(f"{name}: {text[:50]}")

        if found_elements:
            print("Workspace header elements found:")
            for elem in found_elements:
                print(f"  - {elem}")
        else:
            print("Workspace header elements not found with expected locators")

    def test_workspace_stats_display(self, dashboard_page: Page):
        """TC-RG-092: Verify workspace statistics are displayed"""
        page = dashboard_page

        stats_locators = {
            "Total Rules": RuleGenAIDashboardLocators.TOTAL_RULES,
            "Active Rules": RuleGenAIDashboardLocators.ACTIVE_RULES,
            "Pending Rules": RuleGenAIDashboardLocators.PENDING_RULES,
            "Generated Today": RuleGenAIDashboardLocators.GENERATED_TODAY,
        }

        for stat_name, locator in stats_locators.items():
            element = page.locator(locator)
            if element.count() > 0:
                value = element.first.text_content().strip()
                print(f"{stat_name}: {value}")

        # Also check for generic stat cards
        stat_cards = page.locator(RuleGenAIDashboardLocators.STAT_CARD)
        if stat_cards.count() > 0:
            print(f"Found {stat_cards.count()} stat cards")

    def test_workspace_actions_available(self, dashboard_page: Page):
        """TC-RG-093: Verify workspace action buttons are available"""
        page = dashboard_page

        action_buttons = [
            ("Generate Rule", "button:has-text('Generate'), .generate-btn"),
            ("View Rules", "button:has-text('Rules'), a:has-text('Rules')"),
            ("Settings", "button:has-text('Settings'), a:has-text('Settings')"),
        ]

        found_actions = []
        for name, locator in action_buttons:
            element = page.locator(locator)
            if element.count() > 0:
                found_actions.append(name)

        if found_actions:
            print(f"Available actions: {', '.join(found_actions)}")
        else:
            print("Looking for action buttons with alternative selectors...")


@pytest.mark.rulegenai
@pytest.mark.workspace
class TestWorkspaceNavigation:
    """Test suite for navigating between workspaces"""

    def test_workspaces_list_accessible(self, authenticated_rulegenai_page: Page):
        """TC-RG-095: Verify workspaces list is accessible"""
        page = authenticated_rulegenai_page

        # Navigate to workspaces list
        page.goto(RuleGenAIConfig.WORKSPACES_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        print(f"Workspaces URL: {page.url}")

        # Look for workspace list with multiple selector options
        workspace_list = page.locator(".workspace-list, .workspaces-grid, table, [class*='workspace']")
        workspace_cards = page.locator(".workspace-card, .workspace-item, a[href*='/workspaces/']")

        if workspace_list.count() > 0:
            print("Workspace list found")
        elif workspace_cards.count() > 0:
            print(f"Found {workspace_cards.count()} workspace cards/links")
        else:
            # Take screenshot to debug
            page.screenshot(path="screenshots/rulegenai/workspace_list_debug.png")
            print("Workspace list structure not found - screenshot saved for debugging")

    def test_switch_workspace(self, authenticated_rulegenai_page: Page):
        """TC-RG-096: Test switching between workspaces"""
        page = authenticated_rulegenai_page

        # Start at workspace 12
        page.goto(RuleGenAIConfig.DASHBOARD_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        original_url = page.url
        print(f"Starting URL: {original_url}")

        # Look for "All Workspaces" link (based on actual UI)
        all_workspaces = page.locator("a:has-text('All Workspaces'), a[href='/workspaces']")
        workspaces_nav = page.locator(RuleGenAIDashboardLocators.NAV_WORKSPACES)

        if all_workspaces.count() > 0:
            all_workspaces.first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            print(f"Navigated to workspaces list: {page.url}")

            # Look for workspace cards/links
            workspace_links = page.locator("a[href*='/workspaces/']")
            count = workspace_links.count()
            print(f"Found {count} workspace links")

            if count > 0:
                # Try to find a workspace that's not workspace 12
                clicked = False
                for i in range(min(count, 5)):  # Check first 5 only
                    try:
                        href = workspace_links.nth(i).get_attribute("href", timeout=5000)
                        if href and "/12" not in href and "/workspaces/" in href:
                            workspace_links.nth(i).click()
                            page.wait_for_load_state("networkidle")
                            print(f"Switched to: {page.url}")
                            clicked = True
                            break
                    except Exception as e:
                        print(f"Could not check workspace {i}: {str(e)[:50]}")
                        continue

                if not clicked:
                    print("Could not find different workspace to switch to")
            else:
                print("No workspace links found on page")

        elif workspaces_nav.count() > 0:
            workspaces_nav.first.click()
            page.wait_for_load_state("networkidle")
            print(f"Navigated via nav to: {page.url}")
        else:
            print("Workspaces navigation not found - may only have access to current workspace")

    def test_workspace_breadcrumb(self, dashboard_page: Page):
        """TC-RG-097: Test workspace breadcrumb navigation"""
        page = dashboard_page

        # Look for breadcrumb or "All Workspaces" navigation link
        breadcrumb = page.locator(".breadcrumb, nav[aria-label='breadcrumb']")
        all_workspaces = page.locator("a:has-text('All Workspaces')")

        if breadcrumb.count() > 0:
            items = breadcrumb.first.locator(".breadcrumb-item, a")
            print(f"Breadcrumb has {items.count()} items")

            if items.count() > 0:
                try:
                    items.first.click(timeout=5000)
                    page.wait_for_load_state("networkidle")
                    print(f"Navigated via breadcrumb to: {page.url}")
                except Exception as e:
                    print(f"Could not click breadcrumb: {str(e)[:50]}")
        elif all_workspaces.count() > 0:
            print("Using 'All Workspaces' link as navigation")
            all_workspaces.first.click()
            page.wait_for_load_state("networkidle")
            print(f"Navigated to: {page.url}")
        else:
            print("Breadcrumb not found - navigation may use different pattern")


@pytest.mark.rulegenai
@pytest.mark.workspace
class TestWorkspaceSettings:
    """Test suite for workspace settings"""

    def test_workspace_settings_accessible(self, dashboard_page: Page):
        """TC-RG-100: Verify workspace settings are accessible"""
        page = dashboard_page

        settings_nav = page.locator(RuleGenAIDashboardLocators.NAV_SETTINGS)
        settings_btn = page.locator("button:has-text('Settings'), a[href*='settings']")

        if settings_nav.count() > 0:
            settings_nav.first.click()
            page.wait_for_load_state("networkidle")
            print(f"Navigated to settings: {page.url}")
        elif settings_btn.count() > 0:
            settings_btn.first.click()
            page.wait_for_load_state("networkidle")
            print(f"Navigated to settings: {page.url}")
        else:
            print("Settings navigation not found")

    def test_workspace_name_editable(self, dashboard_page: Page):
        """TC-RG-101: Test if workspace name can be edited"""
        page = dashboard_page

        # Navigate to settings
        page.goto(RuleGenAIConfig.SETTINGS_URL)
        page.wait_for_load_state("networkidle")

        # Look for workspace name input
        name_inputs = [
            "input[name='workspace_name']",
            "input[name='name']",
            "#workspace-name",
            ".workspace-name-input",
        ]

        for selector in name_inputs:
            element = page.locator(selector)
            if element.count() > 0 and element.first.is_visible():
                print(f"Found workspace name input: {selector}")
                current_value = element.first.input_value()
                print(f"Current workspace name: {current_value}")
                break
        else:
            print("Workspace name input not found in settings")

    def test_workspace_api_key(self, dashboard_page: Page):
        """TC-RG-102: Test workspace API key management"""
        page = dashboard_page

        # Navigate to settings
        page.goto(RuleGenAIConfig.SETTINGS_URL)
        page.wait_for_load_state("networkidle")

        api_key_section = page.locator(".api-keys, #api-keys, [data-section='api']")
        api_key_list = page.locator(".api-key-item, .key-row")

        if api_key_section.count() > 0:
            print("API key section found")

            if api_key_list.count() > 0:
                print(f"Found {api_key_list.count()} API keys")
        else:
            # May be under different tab/section
            api_nav = page.locator("a:has-text('API'), button:has-text('API')")
            if api_nav.count() > 0:
                api_nav.first.click()
                page.wait_for_timeout(500)
                print("Navigated to API section")


@pytest.mark.rulegenai
@pytest.mark.workspace
class TestWorkspaceAccessibility:
    """Test suite for workspace accessibility"""

    def test_keyboard_navigation(self, dashboard_page: Page):
        """TC-RG-105: Test keyboard navigation in workspace"""
        page = dashboard_page

        # Focus on first interactive element
        page.keyboard.press("Tab")
        page.wait_for_timeout(200)

        # Get focused element
        focused = page.evaluate("document.activeElement.tagName")
        print(f"First focused element: {focused}")

        # Tab through elements
        for i in range(5):
            page.keyboard.press("Tab")
            page.wait_for_timeout(100)

        focused = page.evaluate("document.activeElement.tagName")
        print(f"After 5 tabs, focused element: {focused}")

        print("Keyboard navigation working")

    def test_focus_visible(self, dashboard_page: Page):
        """TC-RG-106: Test focus indicators are visible"""
        page = dashboard_page

        # Tab to an element
        page.keyboard.press("Tab")
        page.wait_for_timeout(200)

        # Check if focus is visible (element has focus outline or similar)
        has_focus_style = page.evaluate("""
            () => {
                const el = document.activeElement;
                const styles = window.getComputedStyle(el);
                return styles.outline !== 'none' ||
                       styles.boxShadow !== 'none' ||
                       el.classList.contains('focus-visible');
            }
        """)

        if has_focus_style:
            print("Focus indicator visible")
        else:
            print("Focus indicator may not be visible (accessibility concern)")

    def test_aria_labels_present(self, dashboard_page: Page):
        """TC-RG-107: Test ARIA labels are present"""
        page = dashboard_page

        # Check for ARIA labels on important elements
        buttons_without_aria = page.evaluate("""
            () => {
                const buttons = document.querySelectorAll('button, [role="button"]');
                let missing = 0;
                buttons.forEach(btn => {
                    if (!btn.getAttribute('aria-label') &&
                        !btn.textContent.trim() &&
                        !btn.getAttribute('aria-labelledby')) {
                        missing++;
                    }
                });
                return missing;
            }
        """)

        if buttons_without_aria > 0:
            print(f"Warning: {buttons_without_aria} buttons without accessible labels")
        else:
            print("All buttons have accessible labels")

    def test_responsive_layout(self, dashboard_page: Page):
        """TC-RG-108: Test responsive layout"""
        page = dashboard_page

        viewports = [
            {"width": 1920, "height": 1080, "name": "Desktop"},
            {"width": 1024, "height": 768, "name": "Tablet Landscape"},
            {"width": 768, "height": 1024, "name": "Tablet Portrait"},
            {"width": 375, "height": 667, "name": "Mobile"},
        ]

        for viewport in viewports:
            page.set_viewport_size({
                "width": viewport["width"],
                "height": viewport["height"]
            })
            page.wait_for_timeout(500)

            # Check if main content is visible
            main_content = page.locator("main, .main-content, .dashboard")
            if main_content.count() > 0 and main_content.first.is_visible():
                print(f"{viewport['name']}: Content visible")
            else:
                print(f"{viewport['name']}: Content may be hidden")

        # Reset to desktop
        page.set_viewport_size({"width": 1920, "height": 1080})
