
class HomePageLocators:
    # Navigation
    DASHBOARD_LINK = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/form/div"
    
    # Main Input Field (handles URL, IP, Domain, Hash)
    MAIN_INPUT = "input[placeholder='URL, IP address, Domain, Hash']"
    
    # File Upload
    FILE_INPUT = "input[type='file']"
    
    # Buttons
    RELOAD_BUTTON = "//button[contains(text(), 'Reload the Query')]"
    SUBMIT_BUTTON = "button[type='submit']"
    
    # Results
    RESULTS_CONTAINER = ".results-container"
    RESULT_ITEM = ".result-item"
    #Url Tools Link
    URL_TOOLS_LINK_BY_TITLE_HREF = "//a[@title='URL Tools' and @href='/url-tools']"
    URL_TOOLS_LINK_BY_SVG_TITLE  = "//a[.//svg[.//title[normalize-space()='Url Tools']]]"
    URL_TOOLS_LINK_NS_SAFE       = "//a[.//*[local-name()='svg']//*[local-name()='title' and normalize-space()='Url Tools']]"

    