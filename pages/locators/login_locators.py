
# pages/login_locators.py
# This file contains only locators. No methods. No logic.

class LoginPageLocators:
    USERNAME = "input[name='username']"
    PASSWORD = "input[type='password']"
    LOGIN_BUTTON = "//button[text()='Login']"
    ERROR_MESSAGE = ".error-message"
    SUCCESS_MESSAGE = ".success-message"
    LOGOUT_BUTTON = "button.logout"
    USER_MENU = "div.user-menu"