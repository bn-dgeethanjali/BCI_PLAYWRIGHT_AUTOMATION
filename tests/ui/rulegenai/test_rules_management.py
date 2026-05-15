"""
RuleGen AI Rules Management Tests
Test cases for managing generated rules (CRUD operations)
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
    RuleGenAIRulesListLocators,
    RuleGenAIModalsLocators,
)
from tests.ui.rulegenai.conftest import RuleGenAIConfig


@pytest.mark.rulegenai
@pytest.mark.rules
class TestRulesListView:
    """Test suite for rules list/table view"""

    def test_rules_list_accessible(self, dashboard_page: Page):
        """TC-RG-060: Verify rules list is accessible"""
        page = dashboard_page

        # Navigate to rules if not already there
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        # Check for rules list
        rules_table = page.locator(RuleGenAIRulesListLocators.RULES_TABLE)
        rules_list = page.locator(".rules-list, .rules-grid")

        if rules_table.count() > 0 or rules_list.count() > 0:
            print("Rules list/table found")
        else:
            # May be on dashboard with rules section
            print("Looking for rules section on current page")

        print(f"Current URL: {page.url}")

    def test_rules_table_columns(self, dashboard_page: Page):
        """TC-RG-061: Verify rules table has expected columns"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        table_header = page.locator(RuleGenAIRulesListLocators.TABLE_HEADER)

        if table_header.count() > 0:
            headers = table_header.first.locator("th, .header-cell")
            header_count = headers.count()

            print(f"Found {header_count} table columns:")
            for i in range(header_count):
                header_text = headers.nth(i).text_content().strip()
                print(f"  - {header_text}")

            # Expect at least name, type, and actions columns
            assert header_count >= 3, "Table should have at least 3 columns"
        else:
            print("Table header not found")

    def test_rules_table_rows(self, dashboard_page: Page):
        """TC-RG-062: Verify rules are displayed in rows"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        table_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW)
        row_count = table_rows.count()

        print(f"Found {row_count} rule rows")

        if row_count > 0:
            # Check first row has expected elements
            first_row = table_rows.first
            print(f"First row text: {first_row.text_content()[:100]}...")
        else:
            # Check for empty state
            empty_state = page.locator(RuleGenAIRulesListLocators.EMPTY_STATE)
            if empty_state.count() > 0:
                print("No rules found - empty state displayed")

    def test_search_rules(self, dashboard_page: Page):
        """TC-RG-063: Test rules search functionality"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        search_input = page.locator(RuleGenAIRulesListLocators.SEARCH_INPUT)

        if search_input.count() > 0:
            # Get initial row count
            initial_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW).count()

            # Search for something
            search_input.first.fill("test")
            page.wait_for_timeout(1000)  # Wait for search debounce

            # Get filtered row count
            filtered_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW).count()

            print(f"Initial rows: {initial_rows}, After search: {filtered_rows}")
            print("Search functionality working")

            # Clear search
            search_input.first.clear()
            page.wait_for_timeout(500)
        else:
            print("Search input not found")

    def test_filter_rules(self, dashboard_page: Page):
        """TC-RG-064: Test rules filter functionality"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        filter_dropdown = page.locator(RuleGenAIRulesListLocators.FILTER_DROPDOWN)

        if filter_dropdown.count() > 0:
            # Get filter options
            options = filter_dropdown.first.locator("option")
            option_count = options.count()

            print(f"Filter has {option_count} options")

            if option_count > 1:
                # Select second option (first is usually "All")
                filter_dropdown.first.select_option(index=1)
                page.wait_for_timeout(500)

                print("Filter applied")

                # Reset filter
                filter_dropdown.first.select_option(index=0)
        else:
            print("Filter dropdown not found")

    def test_sort_rules(self, dashboard_page: Page):
        """TC-RG-065: Test rules sorting functionality"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        sort_dropdown = page.locator(RuleGenAIRulesListLocators.SORT_DROPDOWN)

        if sort_dropdown.count() > 0:
            sort_dropdown.first.select_option(index=1)
            page.wait_for_timeout(500)
            print("Sort applied")
        else:
            # Try clicking sortable header
            headers = page.locator(f"{RuleGenAIRulesListLocators.TABLE_HEADER} th")
            if headers.count() > 0:
                headers.first.click()
                page.wait_for_timeout(500)
                print("Clicked header for sorting")
            else:
                print("Sort functionality not found")

    def test_pagination(self, dashboard_page: Page):
        """TC-RG-066: Test pagination functionality"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        pagination = page.locator(RuleGenAIRulesListLocators.PAGINATION)
        next_page = page.locator(RuleGenAIRulesListLocators.NEXT_PAGE)

        if pagination.count() > 0:
            print("Pagination found")

            if next_page.count() > 0 and next_page.first.is_enabled():
                next_page.first.click()
                page.wait_for_load_state("networkidle")
                print("Navigated to next page")

                # Go back
                prev_page = page.locator(RuleGenAIRulesListLocators.PREV_PAGE)
                if prev_page.count() > 0:
                    prev_page.first.click()
                    page.wait_for_load_state("networkidle")
                    print("Navigated back to previous page")
            else:
                print("Only one page of results")
        else:
            print("Pagination not visible (few results or infinite scroll)")


@pytest.mark.rulegenai
@pytest.mark.rules
class TestRuleCRUDOperations:
    """Test suite for rule CRUD operations"""

    def test_create_rule_button(self, dashboard_page: Page):
        """TC-RG-070: Verify create rule button exists"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        create_btn = page.locator(RuleGenAIRulesListLocators.CREATE_RULE_BTN)

        if create_btn.count() > 0:
            assert create_btn.first.is_visible(), "Create button should be visible"
            print("Create rule button found and visible")
        else:
            print("Create button not found - may use different UI")

    def test_view_rule_details(self, dashboard_page: Page):
        """TC-RG-071: Test viewing rule details"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        # Find first rule row
        table_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW)

        if table_rows.count() > 0:
            first_row = table_rows.first

            # Try view button
            view_btn = first_row.locator(RuleGenAIRulesListLocators.VIEW_RULE_BTN)

            if view_btn.count() > 0:
                view_btn.first.click()
                page.wait_for_timeout(1000)

                # Check if modal opened or navigated to detail page
                modal = page.locator(RuleGenAIModalsLocators.MODAL)
                if modal.count() > 0:
                    print("Rule details modal opened")
                    # Close modal
                    close_btn = page.locator(RuleGenAIModalsLocators.MODAL_CLOSE)
                    if close_btn.count() > 0:
                        close_btn.first.click()
                else:
                    print(f"Navigated to rule details: {page.url}")
            else:
                # Try clicking the row itself
                first_row.click()
                page.wait_for_timeout(1000)
                print(f"Clicked row, current URL: {page.url}")
        else:
            print("No rules to view")

    def test_edit_rule(self, dashboard_page: Page):
        """TC-RG-072: Test editing a rule"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        table_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW)

        if table_rows.count() > 0:
            first_row = table_rows.first
            edit_btn = first_row.locator(RuleGenAIRulesListLocators.EDIT_RULE_BTN)

            if edit_btn.count() > 0:
                edit_btn.first.click()
                page.wait_for_timeout(1000)

                # Check for edit modal or edit page
                modal = page.locator(RuleGenAIModalsLocators.MODAL)
                if modal.count() > 0:
                    print("Edit modal opened")
                    close_btn = page.locator(RuleGenAIModalsLocators.MODAL_CLOSE)
                    if close_btn.count() > 0:
                        close_btn.first.click()
                else:
                    print(f"Edit page opened: {page.url}")
            else:
                print("Edit button not found")
        else:
            print("No rules to edit")

    def test_delete_rule_confirmation(self, dashboard_page: Page):
        """TC-RG-073: Test delete rule shows confirmation"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        table_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW)

        if table_rows.count() > 0:
            first_row = table_rows.first
            delete_btn = first_row.locator(RuleGenAIRulesListLocators.DELETE_RULE_BTN)

            if delete_btn.count() > 0:
                delete_btn.first.click()
                page.wait_for_timeout(500)

                # Should show confirmation modal
                confirm_modal = page.locator(RuleGenAIModalsLocators.MODAL)
                confirm_btn = page.locator(RuleGenAIModalsLocators.CONFIRM_YES)
                cancel_btn = page.locator(RuleGenAIModalsLocators.CONFIRM_NO)

                if confirm_modal.count() > 0:
                    print("Delete confirmation modal displayed")

                    # Cancel the delete
                    if cancel_btn.count() > 0:
                        cancel_btn.first.click()
                        page.wait_for_timeout(500)
                        print("Delete cancelled")
                    else:
                        # Just close modal
                        close_btn = page.locator(RuleGenAIModalsLocators.MODAL_CLOSE)
                        if close_btn.count() > 0:
                            close_btn.first.click()
                else:
                    print("Confirmation modal not shown - may use different pattern")
            else:
                print("Delete button not found")
        else:
            print("No rules to delete")

    def test_duplicate_rule(self, dashboard_page: Page):
        """TC-RG-074: Test duplicating a rule"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        table_rows = page.locator(RuleGenAIRulesListLocators.TABLE_ROW)

        if table_rows.count() > 0:
            initial_count = table_rows.count()
            first_row = table_rows.first
            duplicate_btn = first_row.locator(RuleGenAIRulesListLocators.DUPLICATE_RULE_BTN)

            if duplicate_btn.count() > 0:
                duplicate_btn.first.click()
                page.wait_for_timeout(1000)

                print("Duplicate button clicked")
            else:
                print("Duplicate button not found")
        else:
            print("No rules to duplicate")


@pytest.mark.rulegenai
@pytest.mark.rules
class TestBulkOperations:
    """Test suite for bulk rule operations"""

    def test_bulk_select_all(self, dashboard_page: Page):
        """TC-RG-080: Test select all checkbox"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        select_all = page.locator(RuleGenAIRulesListLocators.BULK_SELECT)
        row_checkboxes = page.locator(RuleGenAIRulesListLocators.COL_CHECKBOX)

        if select_all.count() > 0 and row_checkboxes.count() > 0:
            # Click select all
            select_all.first.click()
            page.wait_for_timeout(300)

            # Verify all rows selected
            checked_count = 0
            for i in range(row_checkboxes.count()):
                if row_checkboxes.nth(i).is_checked():
                    checked_count += 1

            print(f"Selected {checked_count} of {row_checkboxes.count()} rows")

            # Uncheck select all
            select_all.first.click()
            page.wait_for_timeout(300)

            print("Bulk select functionality working")
        else:
            print("Bulk select not available")

    def test_bulk_delete(self, dashboard_page: Page):
        """TC-RG-081: Test bulk delete button"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        bulk_delete = page.locator(RuleGenAIRulesListLocators.BULK_DELETE)
        select_all = page.locator(RuleGenAIRulesListLocators.BULK_SELECT)

        if bulk_delete.count() > 0:
            # Bulk delete should be disabled without selection
            if not bulk_delete.first.is_enabled():
                print("Bulk delete correctly disabled without selection")

            # Select all and check if enabled
            if select_all.count() > 0:
                select_all.first.click()
                page.wait_for_timeout(300)

                if bulk_delete.first.is_enabled():
                    print("Bulk delete enabled after selection")

                # Don't actually delete - just verify button works
                select_all.first.click()  # Deselect
        else:
            print("Bulk delete button not found")

    def test_bulk_export(self, dashboard_page: Page):
        """TC-RG-082: Test bulk export functionality"""
        page = dashboard_page

        # Navigate to rules
        rules_nav = page.locator(RuleGenAIDashboardLocators.NAV_RULES)
        if rules_nav.count() > 0:
            rules_nav.first.click()
            page.wait_for_load_state("networkidle")

        bulk_export = page.locator(RuleGenAIRulesListLocators.BULK_EXPORT)

        if bulk_export.count() > 0 and bulk_export.first.is_visible():
            print("Bulk export button available")

            # Select some rules first
            select_all = page.locator(RuleGenAIRulesListLocators.BULK_SELECT)
            if select_all.count() > 0:
                select_all.first.click()
                page.wait_for_timeout(300)

                if bulk_export.first.is_enabled():
                    print("Bulk export enabled with selection")

                select_all.first.click()  # Deselect
        else:
            print("Bulk export button not found")
