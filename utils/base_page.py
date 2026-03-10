# Minimal BasePage to resolve import error

class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to(self, url):
        self.page.goto(url)

    def wait_for_load_state(self, state="load"):
        self.page.wait_for_load_state(state)

    def fill(self, selector, value):
        self.page.fill(selector, value)

    def click(self, selector):
        self.page.click(selector)

    def press_key(self, selector, key):
        self.page.locator(selector).press(key)

    def is_visible(self, selector):
        return self.page.is_visible(selector)

    def get_text(self, selector):
        return self.page.text_content(selector)

    def get_attribute(self, selector, attr):
        return self.page.get_attribute(selector, attr)
