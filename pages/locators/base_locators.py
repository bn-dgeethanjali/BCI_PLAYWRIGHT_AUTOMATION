"""
Base Page Locators
Contains common locators used across all pages
"""


class BasePageLocators:
    """Common locators for all pages"""
    
    
    # Navigation
    NAV_BAR = "nav, .navbar, .navigation"
    NAV_MENU = ".nav-menu, .menu, ul.navbar-nav"
    NAV_ITEM = ".nav-item, .menu-item"
    NAV_LINK = "a.nav-link, .menu-link"
    
    # Header
    HEADER = "header, .header, .page-header"
    LOGO = ".logo, img.logo, .brand-logo"
    SITE_TITLE = ".site-title, .brand-name"
    
    # Footer
    FOOTER = "footer, .footer, .page-footer"
    COPYRIGHT = ".copyright"
    
    # Common buttons
    SUBMIT_BUTTON = "button[type='submit'], input[type='submit']"
    CANCEL_BUTTON = "button:has-text('Cancel'), .btn-cancel"
    CLOSE_BUTTON = "button.close, .close-btn, [aria-label='Close']"
    BACK_BUTTON = "button:has-text('Back'), .btn-back"
    
    # Common messages
    ALERT = ".alert, [role='alert']"
    ERROR_MESSAGE = ".error, .alert-danger, .error-message"
    SUCCESS_MESSAGE = ".success, .alert-success, .success-message"
    WARNING_MESSAGE = ".warning, .alert-warning"
    INFO_MESSAGE = ".info, .alert-info"
    
    # Loading indicators
    LOADING_SPINNER = ".spinner, .loading, .loader, [data-loading='true']"
    PROGRESS_BAR = ".progress, .progress-bar"
    
    # Modal/Dialog
    MODAL = ".modal, [role='dialog']"
    MODAL_TITLE = ".modal-title, .modal-header h1, .modal-header h2"
    MODAL_BODY = ".modal-body"
    MODAL_FOOTER = ".modal-footer"
    MODAL_CLOSE = ".modal .close, .modal-close"
    
    # Sidebar
    SIDEBAR = "aside, .sidebar, .side-panel"
    SIDEBAR_TOGGLE = ".sidebar-toggle, .menu-toggle"
    
    # Search
    SEARCH_INPUT = "input[type='search'], input[name='search'], .search-input"
    SEARCH_BUTTON = "button[type='search'], .search-btn, button:has-text('Search')"
    SEARCH_RESULTS = ".search-results, .results"
    
    # Tables
    TABLE = "table, .table"
    TABLE_HEADER = "thead, .table-header"
    TABLE_BODY = "tbody, .table-body"
    TABLE_ROW = "tr, .table-row"
    TABLE_CELL = "td, .table-cell"
    
    # Forms
    FORM = "form"
    INPUT_FIELD = "input"
    TEXT_AREA = "textarea"
    SELECT_DROPDOWN = "select"
    CHECKBOX = "input[type='checkbox']"
    RADIO_BUTTON = "input[type='radio']"
    
    # Pagination
    PAGINATION = ".pagination, nav[aria-label='pagination']"
    NEXT_PAGE = ".pagination .next, button:has-text('Next')"
    PREV_PAGE = ".pagination .previous, button:has-text('Previous')"
    PAGE_NUMBER = ".pagination .page-number, .page-link"
    
    # Breadcrumbs
    BREADCRUMB = ".breadcrumb, nav[aria-label='breadcrumb']"
    BREADCRUMB_ITEM = ".breadcrumb-item"
    
    # Tooltips
    TOOLTIP = ".tooltip, [role='tooltip']"
    
    # Dropdowns
    DROPDOWN = ".dropdown, [role='menu']"
    DROPDOWN_TOGGLE = ".dropdown-toggle"
    DROPDOWN_MENU = ".dropdown-menu"
    DROPDOWN_ITEM = ".dropdown-item, [role='menuitem']"
    
    # Tabs
    TAB_LIST = ".nav-tabs, [role='tablist']"
    TAB = ".nav-link, [role='tab']"
    TAB_PANEL = ".tab-pane, [role='tabpanel']"
    
    # Cards
    CARD = ".card"
    CARD_HEADER = ".card-header"
    CARD_BODY = ".card-body"
    CARD_FOOTER = ".card-footer"
    
    # Badges
    BADGE = ".badge, .label"
    
    # Icons
    ICON = ".icon, i, svg[class*='icon']"
