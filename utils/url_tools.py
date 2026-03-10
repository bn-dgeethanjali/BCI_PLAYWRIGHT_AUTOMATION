from pages.locators.url_tools_locators import URLToolsLocators

class URLToolsPage:
    """Page object for URL Tools UI automation."""
    def __init__(self, page):
        self.page = page
        self.locators = URLToolsLocators

    def navigate(self):
        self.page.goto("/url-tools")

    def submit_url(self, url):
        self.page.fill(self.locators.URL_INPUT, url)
        self.page.wait_for_selector(self.locators.URL_INPUT, state="visible", timeout=10000)
        self.page.press(self.locators.URL_INPUT, "Enter")

    def get_results(self):
        return self.page.query_selector(self.locators.RESULTS_CONTAINER)

    def is_on_url_tools_page(self):
        """Check if current page is URL Tools page by verifying input visibility."""
        return self.page.is_visible(self.locators.URL_INPUT)

    def is_input_visible(self):
        """Check if the input field is visible on the page."""
        return self.page.is_visible(self.locators.URL_INPUT)

    def clear_input(self):
        """Clear the input field."""
        self.page.fill(self.locators.URL_INPUT, "")

    def enter_url(self, url):
        """Enter a URL into the input field without submitting."""
        self.page.fill(self.locators.URL_INPUT, url)

    def get_input_value(self):
        """Get the current value of the input field."""
        return self.page.input_value(self.locators.URL_INPUT)
