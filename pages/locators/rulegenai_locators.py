"""
RuleGen AI Dashboard Locators
Contains all locators for the RuleGen AI application pages
"""


class RuleGenAILoginLocators:
    """Locators for the RuleGen AI Login Page"""

    # Login Form - Updated based on actual page inspection
    USERNAME_INPUT = "#username, input[name='username']"
    PASSWORD_INPUT = "#password, input[type='password']"
    LOGIN_BUTTON = "button[type='submit'], button:has-text('Sign in')"
    REMEMBER_ME = "#remember-me, input[name='remember-me']"
    FORGOT_PASSWORD = "a:has-text('Forgot'), a[href*='forgot'], .forgot-password"

    # Messages
    ERROR_MESSAGE = ".error, .alert-error, .login-error, [role='alert']"
    SUCCESS_MESSAGE = ".success, .alert-success"

    # SSO/OAuth
    SSO_BUTTON = "button:has-text('SSO'), button:has-text('Single Sign'), .sso-login"
    OAUTH_GOOGLE = "button:has-text('Google'), .google-login"
    OAUTH_MICROSOFT = "button:has-text('Microsoft'), .microsoft-login"


class RuleGenAIDashboardLocators:
    """Locators for the RuleGen AI Dashboard/Workspace Page"""

    # Header & Navigation
    HEADER = "header, .header, .app-header"
    NAV_BAR = "nav, .navbar, .navigation"
    LOGO = ".logo, img.logo, .brand"
    USER_MENU = ".user-menu, .profile-dropdown, .avatar"
    LOGOUT_BUTTON = "button:has-text('Logout'), a:has-text('Logout'), #logout"

    # Sidebar Navigation
    SIDEBAR = "aside, .sidebar, .side-nav"
    NAV_DASHBOARD = "a[href*='dashboard'], a:has-text('Dashboard')"
    NAV_WORKSPACES = "a[href*='workspaces'], a:has-text('Workspaces')"
    NAV_RULES = "a[href*='rules'], a:has-text('Rules')"
    NAV_MODELS = "a[href*='models'], a:has-text('Models')"
    NAV_HISTORY = "a[href*='history'], a:has-text('History')"
    NAV_SETTINGS = "a[href*='settings'], a:has-text('Settings')"

    # Workspace Header
    WORKSPACE_TITLE = ".workspace-title, .workspace-name, h1, .page-title"
    WORKSPACE_ID = ".workspace-id, [data-workspace-id], .workspace-meta"
    WORKSPACE_DESCRIPTION = ".workspace-description, .description"
    WORKSPACE_STATUS = ".workspace-status, .status-badge"

    # Stats/Metrics Cards
    STATS_CONTAINER = ".stats, .metrics, .dashboard-stats"
    STAT_CARD = ".stat-card, .metric-card, .kpi-card"
    TOTAL_RULES = "[data-stat='total-rules'], .total-rules"
    ACTIVE_RULES = "[data-stat='active-rules'], .active-rules"
    PENDING_RULES = "[data-stat='pending-rules'], .pending-rules"
    GENERATED_TODAY = "[data-stat='generated-today'], .today-count"


class RuleGenAIRuleGeneratorLocators:
    """Locators for the Rule Generation Interface (Multi-step Wizard)"""

    # Main Tabs
    TAB_RULE_GENERATION = "button:has-text('Rule Generation')"
    TAB_PROMPT_MANAGEMENT = "button:has-text('Prompt Management')"

    # Wizard Steps (4-step workflow)
    STEP_UPLOAD_EMAILS = "button:has-text('Upload Emails'), [data-step='upload']"
    STEP_SELECT_HEADERS = "button:has-text('Select Headers'), [data-step='headers']"
    STEP_CONFIGURE_PROMPT = "button:has-text('Configure Prompt'), [data-step='prompt']"
    STEP_GENERATE_RULES = "button:has-text('Generate Rules'), [data-step='generate']"

    # Token Usage Section
    TOKEN_USAGE = ".token-usage, [class*='token']"

    # Input Section (in Configure Prompt step)
    PROMPT_INPUT = "textarea, .prompt-input, #rule-input, [class*='prompt'] textarea"
    PROMPT_PLACEHOLDER = "textarea::placeholder"
    CHAR_COUNTER = ".char-count, .character-counter"
    CLEAR_INPUT_BTN = "button:has-text('Clear'), .clear-btn, #clear-input"

    # AI Model Selection
    MODEL_SELECTOR = "select#model, .model-select, [data-testid='model-selector']"
    MODEL_OPTION = ".model-option, option"
    MODEL_INFO = ".model-info, .model-description"

    # Configuration Options
    CONFIG_PANEL = ".config-panel, .options-panel, .settings"
    SEVERITY_SELECTOR = "select#severity, .severity-select"
    RULE_TYPE_SELECTOR = "select#rule-type, .rule-type-select"
    OUTPUT_FORMAT = "select#format, .format-select"

    # Generation Controls
    GENERATE_BUTTON = "button:has-text('Generating'), button:has-text('Generate Rules'), button:has-text('Generate')"
    STOP_BUTTON = "button:has-text('Stop'), button#stop, .stop-btn"
    REGENERATE_BUTTON = "button:has-text('Regenerate Rule'), button:has-text('Regenerate')"
    BACK_TO_PROMPT_CONFIG = "button:has-text('Back to Prompt Configuration')"

    # Output Section - Generated Rule
    OUTPUT_CONTAINER = ".generated-rule, [class*='generated'], .output-container"
    RULE_OUTPUT = "pre, code, .rule-content, [class*='rule'] pre"
    RULE_TITLE = "h2:has-text('Generated Rule'), h3:has-text('Rule')"
    RULE_PAGINATION = "[class*='pagination'], .rule-nav"
    RULE_COUNT = "text=/Rule \\d+ of \\d+/, text=/Rule \\d\\/\\d/"
    OUTPUT_CODE = "code, pre, .code-block"
    COPY_BUTTON = "button:has-text('Copy'), .copy-btn, [data-action='copy']"
    DOWNLOAD_BUTTON = "button:has-text('Download'), .download-btn"
    EXPORT_RULES_BUTTON = "button:has-text('Export Rules')"
    SAVE_BUTTON = "button:has-text('Save'), .save-btn, #save-rule"

    # Loading States
    LOADING_INDICATOR = ".loading, .generating, .spinner, [class*='loading']"
    PROGRESS_BAR = ".progress, .progress-bar"
    GENERATION_STATUS = ".generation-status, .status-text"

    # Validation & Feedback
    VALIDATION_RESULT = ".validation-result, .validation-status"
    VALIDATION_ERRORS = ".validation-errors, .errors"
    VALIDATION_WARNINGS = ".validation-warnings, .warnings"
    FEEDBACK_INPUT = "textarea[placeholder*='feedback'], .feedback-input"
    FEEDBACK_THUMBS_UP = "button[aria-label='Good'], .thumbs-up"
    FEEDBACK_THUMBS_DOWN = "button[aria-label='Bad'], .thumbs-down"

    # Share functionality
    SHARE_BUTTON = "button:has-text('Share')"
    SHOW_PROMPT_BUTTON = "button:has-text('Show Prompt')"


class RuleGenAIRulesListLocators:
    """Locators for the Rules List/Management Page"""

    # List Controls
    SEARCH_INPUT = "input[type='search'], input[placeholder*='Search'], .search-input"
    FILTER_DROPDOWN = ".filter-dropdown, select.filter"
    SORT_DROPDOWN = ".sort-dropdown, select.sort"
    VIEW_TOGGLE = ".view-toggle, .list-grid-toggle"

    # Rules Table
    RULES_TABLE = "table.rules, .rules-table, .rules-list"
    TABLE_HEADER = "thead, .table-header"
    TABLE_ROW = "tbody tr, .rule-row, .rule-item"

    # Table Columns
    COL_CHECKBOX = "input[type='checkbox'], .row-select"
    COL_NAME = ".rule-name, td:nth-child(2)"
    COL_TYPE = ".rule-type, td:nth-child(3)"
    COL_SEVERITY = ".rule-severity, td:nth-child(4)"
    COL_STATUS = ".rule-status, td:nth-child(5)"
    COL_CREATED = ".rule-created, td:nth-child(6)"
    COL_ACTIONS = ".rule-actions, td:last-child"

    # Actions
    CREATE_RULE_BTN = "button:has-text('Create'), button:has-text('New Rule'), #create-rule"
    BULK_SELECT = "input#select-all, .select-all"
    BULK_DELETE = "button:has-text('Delete Selected'), .bulk-delete"
    BULK_EXPORT = "button:has-text('Export'), .bulk-export"

    # Row Actions
    EDIT_RULE_BTN = "button[aria-label='Edit'], .edit-btn, [data-action='edit']"
    DELETE_RULE_BTN = "button[aria-label='Delete'], .delete-btn, [data-action='delete']"
    VIEW_RULE_BTN = "button[aria-label='View'], .view-btn, [data-action='view']"
    DUPLICATE_RULE_BTN = "button[aria-label='Duplicate'], .duplicate-btn"

    # Pagination
    PAGINATION = ".pagination, nav[aria-label='pagination']"
    PAGE_INFO = ".page-info, .pagination-info"
    PREV_PAGE = "button:has-text('Previous'), .prev-page"
    NEXT_PAGE = "button:has-text('Next'), .next-page"
    PAGE_SIZE = "select.page-size, .items-per-page"

    # Empty State
    EMPTY_STATE = ".empty-state, .no-rules"
    EMPTY_MESSAGE = ".empty-message"


class RuleGenAIModalsLocators:
    """Locators for Modal Dialogs"""

    # Generic Modal
    MODAL = ".modal, [role='dialog'], .dialog"
    MODAL_OVERLAY = ".modal-overlay, .modal-backdrop"
    MODAL_HEADER = ".modal-header, .dialog-header"
    MODAL_TITLE = ".modal-title, .dialog-title, h2"
    MODAL_BODY = ".modal-body, .dialog-body"
    MODAL_FOOTER = ".modal-footer, .dialog-footer"
    MODAL_CLOSE = "button.close, .modal-close, [aria-label='Close']"

    # Confirmation Modal
    CONFIRM_TITLE = ".confirm-title"
    CONFIRM_MESSAGE = ".confirm-message"
    CONFIRM_YES = "button:has-text('Yes'), button:has-text('Confirm'), .confirm-btn"
    CONFIRM_NO = "button:has-text('No'), button:has-text('Cancel'), .cancel-btn"

    # Rule Preview Modal
    PREVIEW_TITLE = ".preview-title"
    PREVIEW_CONTENT = ".preview-content, pre"
    PREVIEW_CLOSE = "button:has-text('Close'), .close-preview"

    # Save Rule Modal
    SAVE_RULE_NAME = "input#rule-name, input[name='name']"
    SAVE_RULE_DESC = "textarea#description, textarea[name='description']"
    SAVE_RULE_TAGS = "input#tags, .tags-input"
    SAVE_RULE_SUBMIT = "button:has-text('Save'), button[type='submit']"


class RuleGenAISettingsLocators:
    """Locators for Settings Page"""

    # Settings Navigation
    SETTINGS_NAV = ".settings-nav, .settings-sidebar"
    NAV_PROFILE = "a:has-text('Profile'), .settings-profile"
    NAV_API_KEYS = "a:has-text('API Keys'), .settings-api"
    NAV_PREFERENCES = "a:has-text('Preferences'), .settings-prefs"
    NAV_NOTIFICATIONS = "a:has-text('Notifications'), .settings-notif"

    # Profile Settings
    PROFILE_NAME = "input#name, input[name='name']"
    PROFILE_EMAIL = "input#email, input[name='email']"
    PROFILE_AVATAR = ".avatar-upload, input[type='file']"
    SAVE_PROFILE = "button:has-text('Save Profile'), #save-profile"

    # API Keys
    API_KEY_LIST = ".api-keys, .keys-list"
    API_KEY_ITEM = ".api-key-item, .key-row"
    CREATE_API_KEY = "button:has-text('Create'), #create-key"
    REVOKE_API_KEY = "button:has-text('Revoke'), .revoke-key"
    COPY_API_KEY = "button:has-text('Copy'), .copy-key"

    # Preferences
    THEME_SELECTOR = "select#theme, .theme-select"
    LANGUAGE_SELECTOR = "select#language, .language-select"
    DEFAULT_MODEL = "select#default-model"
    AUTO_SAVE = "input#auto-save, .auto-save-toggle"
