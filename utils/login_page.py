from utils.base_page import BasePage
from playwright.sync_api import Page
from pages.locators.login_locators import LoginPageLocators


class LoginPage(BasePage):
    """
    Login Page Object for MailXray application
    Contains only action methods - locators are in LoginPageLocators
    """
    
    # Import locators for easy access
    locators = LoginPageLocators
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def navigate(self):
        """Navigate to login page"""
        self.navigate_to("/accounts/login/")
        self.wait_for_load_state()
    
    def login(self, username: str, password: str):
        """Perform login action"""
        self.fill(self.locators.USERNAME_INPUT, username)
        self.fill(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        self.wait_for_load_state()
    
    def login_with_enter_key(self, username: str, password: str):
        """Perform login using Enter key"""
        self.fill(self.locators.USERNAME_INPUT, username)
        self.fill(self.locators.PASSWORD_INPUT, password)
        self.press_key(self.locators.PASSWORD_INPUT, "Enter")
        self.wait_for_load_state()
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible(self.locators.ERROR_MESSAGE)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_error_displayed():
            return self.get_text(self.locators.ERROR_MESSAGE)
        return ""
    
    def is_success_displayed(self) -> bool:
        """Check if success message is displayed"""
        return self.is_visible(self.locators.SUCCESS_MESSAGE)
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        # Check for logout button or user menu presence
        return self.is_visible(self.locators.LOGOUT_BUTTON) or self.is_visible(self.locators.USER_MENU)
    
    def logout(self):
        """Perform logout action"""
        if self.is_visible(self.locators.USER_MENU):
            self.click(self.locators.USER_MENU)
        self.click(self.locators.LOGOUT_BUTTON)
        self.wait_for_load_state()
    
    def clear_username(self):
        """Clear username field"""
        self.page.locator(self.locators.USERNAME_INPUT).clear()
    
    def clear_password(self):
        """Clear password field"""
        self.page.locator(self.locators.PASSWORD_INPUT).clear()
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        return self.page.locator(self.locators.LOGIN_BUTTON).is_enabled()
    
    def get_username_placeholder(self) -> str:
        """Get username input placeholder text"""
        return self.get_attribute(self.locators.USERNAME_INPUT, "placeholder") or ""
    
    def get_password_placeholder(self) -> str:
        """Get password input placeholder text"""
        return self.get_attribute(self.locators.PASSWORD_INPUT, "placeholder") or ""
    
    def click_forgot_password(self):
        """Click forgot password link"""
        if self.is_visible(self.locators.FORGOT_PASSWORD_LINK):
            self.click(self.locators.FORGOT_PASSWORD_LINK)
            self.wait_for_load_state()
    
    def click_signup(self):
        """Click signup/register link"""
        if self.is_visible(self.locators.SIGNUP_LINK):
            self.click(self.locators.SIGNUP_LINK)
            self.wait_for_load_state()
    
    def check_remember_me(self):
        """Check remember me checkbox"""
        if self.is_visible(self.locators.REMEMBER_ME_CHECKBOX):
            self.check(self.locators.REMEMBER_ME_CHECKBOX)
    
    def uncheck_remember_me(self):
        """Uncheck remember me checkbox"""
        if self.is_visible(self.locators.REMEMBER_ME_CHECKBOX):
            self.uncheck(self.locators.REMEMBER_ME_CHECKBOX)
