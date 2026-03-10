from playwright.sync_api import Page
from pages.locators.homepage_locator import HomePageLocators

class HomePage:
    """Page object for MailXray homepage UI automation."""
    locators = HomePageLocators

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/")
        self.page.wait_for_load_state()

    def submit_url(self, url):
        self.page.fill(self.locators.MAIN_INPUT, url)
        self.page.click(self.locators.SUBMIT_BUTTON)

    def submit_ip(self, ip):
        self.page.fill(self.locators.MAIN_INPUT, ip)
        self.page.click(self.locators.SUBMIT_BUTTON)

    def submit_domain(self, domain):
        self.page.fill(self.locators.MAIN_INPUT, domain)
        self.page.click(self.locators.SUBMIT_BUTTON)

    def clear_input(self):
        self.page.fill(self.locators.MAIN_INPUT, "")
