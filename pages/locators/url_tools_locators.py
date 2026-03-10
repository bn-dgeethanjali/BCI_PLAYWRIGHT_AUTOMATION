# url_tools_locators.py
# This file contains only locators for URL Tools page. No methods. No logic.

class URLToolsLocators:
    # Main Input Field
    URL_INPUT = "input[placeholder='Enter URL']"
    
    # Buttons
    SUBMIT_BUTTON = "button[type='submit']"
    COPY_BUTTON = "//button[contains(text(), 'Copy to Clipboard')]"
    RELOAD_BUTTON = "//button[contains(text(), 'Reload the Query')]"
    
    # URL Tools Features - Tabs/Links
    URL_UNQUOTE = "a[href='/url-tools/url-unquote'][data-discover='true']"
    URL_PROTECT = "//a[contains(text(), 'URL Protect')] | //div[contains(text(), 'URL Protect')]"
    DEFANGED_URL = "//a[contains(text(), 'Defanged URL')] | //div[contains(text(), 'Defanged URL')]"
    URL_REDIRECT = "//a[contains(text(), 'Url Redirect')] | //div[contains(text(), 'Url Redirect')]"
    
    # Results/Output sections
    RESULTS_CONTAINER = ".results-container"
    RESULT_ITEM = ".result-item"
    OUTPUT_AREA = "//div[contains(@class, 'mt-5') or contains(@class, 'result')]"
