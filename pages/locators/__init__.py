"""
Locators package for page objects.
Centralizes all UI element selectors.
"""

from pages.locators.base_locators import BasePageLocators
from pages.locators.login_locators import LoginPageLocators
from pages.locators.dashboard_locators import DashboardPageLocators
from pages.locators.reports_locators import ReportsPageLocators

__all__ = [
    'BasePageLocators',
    'LoginPageLocators',
    'DashboardPageLocators',
    'ReportsPageLocators',
]
