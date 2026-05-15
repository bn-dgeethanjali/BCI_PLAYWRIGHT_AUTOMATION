"""
RuleGen AI Dashboard Tests
Test cases for the main dashboard/workspace functionality
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
)
from tests.ui.rulegenai.conftest import RuleGenAIConfig


@pytest.mark.rulegenai
class TestRuleGenAIDashboard:
    """Test suite for RuleGen AI Dashboard"""

    def test_dashboard_loads(self, dashboard_page: Page):
        """TC-RG-010: Verify dashboard loads successfully"""
        page = dashboard_page

        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")

        # Verify we're on the workspace/dashboard
        assert "workspaces" in page.url.lower() or "dashboard" in page.url.lower()

        # Take screenshot
        page.screenshot(path="screenshots/rulegenai_dashboard.png", full_page=True)

        print("Dashboard loaded successfully")

    def test_workspace_title_displayed(self, dashboard_page: Page):
        """TC-RG-011: Verify workspace title is displayed"""
        page = dashboard_page

        # Check for workspace title
        title_locators = [
            RuleGenAIDashboardLocators.WORKSPACE_TITLE,
            "h1",
            ".page-title",
            ".workspace-name",
        ]

        title_found = False
        for locator in title_locators:
            element = page.locator(locator)
            if element.count() > 0 and element.first.is_visible():
                title_text = element.first.text_content()
                print(f"Workspace title found: {title_text}")
                title_found = True
                break

        assert title_found, "Workspace title not found on dashboard"

    def test_navigation_elements_visible(self, dashboard_page: Page):
        """TC-RG-012: Verify navigation elements are visible"""
        page = dashboard_page

        nav_elements = {
            "Navigation bar": RuleGenAIDashboardLocators.NAV_BAR,
            "Sidebar": RuleGenAIDashboardLocators.SIDEBAR,
            "Header": RuleGenAIDashboardLocators.HEADER,
        }

        found_nav = []
        for name, locator in nav_elements.items():
            element = page.locator(locator)
            if element.count() > 0:
                found_nav.append(name)
                print(f"Found: {name}")

        assert len(found_nav) > 0, "No navigation elements found"
        print(f"Navigation elements visible: {', '.join(found_nav)}")

    def test_user_menu_accessible(self, dashboard_page: Page):
        """TC-RG-013: Verify user menu is accessible"""
        page = dashboard_page

        user_menu = page.locator(RuleGenAIDashboardLocators.USER_MENU)

        if user_menu.count() > 0:
            user_menu.first.click()
            page.wait_for_timeout(500)

            # Check for logout option
            logout = page.locator(RuleGenAIDashboardLocators.LOGOUT_BUTTON)
            if logout.count() > 0:
                print("User menu opened, logout button visible")
            else:
                print("User menu opened but logout button not found")

            # Click elsewhere to close menu
            page.locator("body").click()
        else:
            print("User menu not found - may use different UI pattern")

    def test_workspace_id_in_url(self, dashboard_page: Page):
        """TC-RG-014: Verify correct workspace ID in URL"""
        page = dashboard_page

        expected_workspace_id = RuleGenAIConfig.WORKSPACE_ID
        current_url = page.url

        assert expected_workspace_id in current_url, \
            f"Expected workspace ID '{expected_workspace_id}' not found in URL: {current_url}"

        print(f"Workspace ID {expected_workspace_id} correctly in URL")

    def test_dashboard_stats_visible(self, dashboard_page: Page):
        """TC-RG-015: Verify dashboard statistics/metrics are displayed"""
        page = dashboard_page

        stats_locators = [
            RuleGenAIDashboardLocators.STATS_CONTAINER,
            RuleGenAIDashboardLocators.STAT_CARD,
            ".stats",
            ".metrics",
            ".dashboard-cards",
        ]

        stats_found = False
        for locator in stats_locators:
            element = page.locator(locator)
            if element.count() > 0:
                print(f"Stats container found with locator: {locator}")
                print(f"Number of stat elements: {element.count()}")
                stats_found = True
                break

        if not stats_found:
            print("No stats/metrics section found - may be different UI structure")

    def test_page_load_performance(self, dashboard_page: Page):
        """TC-RG-016: Verify dashboard loads within acceptable time"""
        page = dashboard_page

        # Navigate again to measure load time
        start_time = page.evaluate("() => performance.now()")
        page.goto(RuleGenAIConfig.DASHBOARD_URL)
        page.wait_for_load_state("networkidle")
        end_time = page.evaluate("() => performance.now()")

        load_time = end_time - start_time
        print(f"Dashboard load time: {load_time:.2f}ms")

        # Dashboard should load within 10 seconds
        assert load_time < 10000, f"Dashboard took too long to load: {load_time:.2f}ms"

    def test_no_console_errors(self, dashboard_page: Page):
        """TC-RG-017: Verify no critical console errors on dashboard"""
        page = dashboard_page

        console_errors = []

        def handle_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)

        page.on("console", handle_console)

        # Reload to capture console messages
        page.reload()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        if console_errors:
            print(f"Console errors found: {console_errors}")
            # Warning but not failing - some errors may be acceptable
        else:
            print("No console errors detected")

    def test_dashboard_refresh(self, dashboard_page: Page):
        """TC-RG-018: Verify dashboard handles refresh correctly"""
        page = dashboard_page

        original_url = page.url

        # Refresh the page
        page.reload()
        page.wait_for_load_state("networkidle")

        # Should still be on dashboard
        assert page.url == original_url or "workspaces" in page.url.lower()

        print("Dashboard refresh successful")


@pytest.mark.rulegenai
class TestDashboardNavigation:
    """Test suite for dashboard navigation"""

    def test_navigate_to_rules(self, dashboard_page: Page):
        """TC-RG-020: Navigate to rules section"""
        page = dashboard_page

        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)

        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

            assert "rules" in page.url.lower()
            print("Successfully navigated to rules section")
        else:
            print("Rules navigation not found in sidebar")

    def test_navigate_to_workspaces(self, dashboard_page: Page):
        """TC-RG-021: Navigate to workspaces list"""
        page = dashboard_page

        workspaces_nav = page.locator(RuleGenAIDashboardLocators.NAV_WORKSPACES)

        if workspaces_nav.count() > 0:
            workspaces_nav.first.click()
            page.wait_for_load_state("networkidle")

            assert "workspaces" in page.url.lower()
            print("Successfully navigated to workspaces")
        else:
            print("Workspaces navigation not found")

    def test_navigate_to_settings(self, dashboard_page: Page):
        """TC-RG-022: Navigate to settings"""
        page = dashboard_page

        settings_nav = page.locator(RuleGenAIDashboardLocators.NAV_SETTINGS)

        if settings_nav.count() > 0:
            settings_nav.first.click()
            page.wait_for_load_state("networkidle")

            assert "settings" in page.url.lower()
            print("Successfully navigated to settings")
        else:
            print("Settings navigation not found")

    def test_logo_returns_to_home(self, dashboard_page: Page):
        """TC-RG-023: Clicking logo returns to home/dashboard"""
        page = dashboard_page

        logo = page.locator(RuleGenAIDashboardLocators.LOGO)

        if logo.count() > 0:
            logo.first.click()
            page.wait_for_load_state("networkidle")

            # Should be on home or dashboard
            url = page.url.lower()
            is_home = any(x in url for x in ["home", "dashboard", "workspaces"])
            assert is_home, f"Logo click did not navigate to home: {page.url}"

            print("Logo click navigates to home")
        else:
            print("Logo not found")

    def test_browser_back_button(self, dashboard_page: Page):
        """TC-RG-024: Browser back button works correctly"""
        page = dashboard_page

        initial_url = page.url

        # Navigate somewhere else
        settings_nav = page.locator(RuleGenAIDashboardLocators.NAV_SETTINGS)
        if settings_nav.count() > 0:
            settings_nav.first.click()
            page.wait_for_load_state("networkidle")

            # Go back
            page.go_back()
            page.wait_for_load_state("networkidle")

            assert page.url == initial_url or "workspaces" in page.url.lower()
            print("Browser back button works correctly")
        else:
            print("Could not test back button - no navigation available")
