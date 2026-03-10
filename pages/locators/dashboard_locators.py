"""
Dashboard Page Locators
Contains all locators for the dashboard page
"""


class DashboardPageLocators:
    """Locators for Dashboard Page elements"""
    
    # Main sections
    DASHBOARD_CONTAINER = ".dashboard, #dashboard, main.dashboard"
    DASHBOARD_TITLE = "h1.dashboard-title, .page-title"
    
    # Tools/Services cards
    TOOLS_SECTION = ".tools-section, #tools, .services"
    TOOL_CARD = ".tool-card, .service-card, .card"
    TOOL_TITLE = ".tool-title, .card-title"
    TOOL_DESCRIPTION = ".tool-description, .card-text"
    TOOL_LINK = ".tool-link, .card-link, a"
    
    # Individual tool links
    WHOIS_TOOL = "a[href*='whois'], .tool-whois"
    MX_LOOKUP_TOOL = "a[href*='mxlookup'], .tool-mxlookup"
    VIRUSTOTAL_TOOL = "a[href*='virustotal'], .tool-virustotal"
    EML_DATA_TOOL = "a[href*='emldata'], .tool-emldata"
    PHAAS_TOOL = "a[href*='phaas'], .tool-phaas"
    BLOCKLIST_TOOL = "a[href*='blocklist'], .tool-blocklist"
    
    # Statistics/Metrics
    STATS_SECTION = ".stats, .metrics, .statistics"
    STAT_CARD = ".stat-card, .metric"
    STAT_VALUE = ".stat-value, .metric-value"
    STAT_LABEL = ".stat-label, .metric-label"
    
    # Recent activity
    RECENT_ACTIVITY = ".recent-activity, .activity-feed"
    ACTIVITY_ITEM = ".activity-item, .activity"
    ACTIVITY_TIME = ".activity-time, .timestamp"
    ACTIVITY_DESCRIPTION = ".activity-description"
    
    # Quick actions
    QUICK_ACTIONS = ".quick-actions"
    QUICK_ACTION_BUTTON = ".quick-action, .action-btn"
    
    # User info
    USER_INFO = ".user-info, .user-profile"
    USER_NAME = ".user-name, .username"
    USER_EMAIL = ".user-email"
    USER_ROLE = ".user-role"
    
    # Notifications
    NOTIFICATION_BELL = ".notification-icon, .notifications"
    NOTIFICATION_COUNT = ".notification-count, .badge"
    NOTIFICATION_DROPDOWN = ".notification-dropdown, .notifications-menu"
    NOTIFICATION_ITEM = ".notification-item"
