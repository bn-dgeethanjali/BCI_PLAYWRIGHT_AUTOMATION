"""
Reports Page Locators
Contains all locators for the reports page
"""


class ReportsPageLocators:
    """Locators for Reports Page elements"""
    
    # Page elements
    PAGE_TITLE = "h1, .page-title, .reports-title"
    PAGE_DESCRIPTION = ".page-description"
    
    # Filters section
    FILTERS_SECTION = ".filters, .filter-panel"
    DATE_FILTER = "input[type='date'], .date-filter"
    START_DATE = "input[name='start_date'], #start-date"
    END_DATE = "input[name='end_date'], #end-date"
    SEARCH_FILTER = "input[type='search'], .search-filter"
    CATEGORY_FILTER = "select[name='category'], .category-filter"
    STATUS_FILTER = "select[name='status'], .status-filter"
    APPLY_FILTERS = "button:has-text('Apply'), .apply-filters"
    RESET_FILTERS = "button:has-text('Reset'), .reset-filters"
    
    # Reports table
    REPORTS_TABLE = "table.reports, .reports-table"
    TABLE_HEADER = "thead, .table-header"
    TABLE_BODY = "tbody, .table-body"
    TABLE_ROW = "tr, .table-row"
    REPORT_ITEM = ".report-item, tr"
    
    # Table columns
    REPORT_NAME = "td.report-name, .name-column"
    REPORT_DATE = "td.report-date, .date-column"
    REPORT_TYPE = "td.report-type, .type-column"
    REPORT_STATUS = "td.report-status, .status-column"
    REPORT_ACTIONS = "td.actions, .action-column"
    
    # Action buttons
    VIEW_REPORT = "button:has-text('View'), a:has-text('View')"
    DOWNLOAD_REPORT = "button:has-text('Download'), a:has-text('Download')"
    DELETE_REPORT = "button:has-text('Delete'), .delete-btn"
    SHARE_REPORT = "button:has-text('Share'), .share-btn"
    EXPORT_REPORT = "button:has-text('Export'), .export-btn"
    
    # Create/Generate report
    CREATE_REPORT_BTN = "button:has-text('Create Report'), .create-report"
    GENERATE_REPORT_BTN = "button:has-text('Generate'), .generate-report"
    
    # Pagination
    PAGINATION = ".pagination"
    NEXT_PAGE = ".next, button:has-text('Next')"
    PREV_PAGE = ".previous, button:has-text('Previous')"
    PAGE_INFO = ".page-info, .pagination-info"
    
    # Empty state
    NO_REPORTS_MESSAGE = ".no-reports, .empty-state"
    
    # Report details modal
    REPORT_MODAL = ".modal, .report-details"
    MODAL_TITLE = ".modal-title"
    MODAL_CONTENT = ".modal-body, .report-content"
    MODAL_CLOSE = ".close, .modal-close"
