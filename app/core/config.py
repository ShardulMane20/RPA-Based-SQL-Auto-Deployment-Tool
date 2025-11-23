"""
Application Configuration
Contains all constants, colors, fonts, and settings for the SQL Tool application
"""

import os

class AppConfig:
    """Main application configuration class"""
    
    # =============================================================================
    # APPLICATION CONSTANTS
    # =============================================================================
    
    APP_TITLE = "Zanvar's SQL Tool"
    APP_GEOMETRY = "1200x900"
    HISTORY_FILE = "query_history.pkl"
    MAX_HISTORY_ENTRIES = 50
    ASSETS_DIR = "assets"
    LOGO_FILENAME = "logo.png"
    
    # =============================================================================
    # DATABASE SETTINGS
    # =============================================================================
    
    DEFAULT_SERVER = "localhost\\SQLEXPRESS"
    DEFAULT_USERNAME = "sa"
    DEFAULT_PASSWORD = ""
    CONNECTION_TIMEOUT = 10
    QUERY_BATCH_SIZE = 1000
    
    # =============================================================================
    # COLOR SCHEME
    # =============================================================================
    
    COLORS = {
        # Main background and UI colors
        'bg_color': "#f5f5f5",
        'primary_color': "#2c3e50",
        'muted_color': "#7f8c8d",
        'success_color': "#27ae60",
        'accent_color': "#3498db",
        'border_color': "#bdc3c7",
        'card_bg': "#ffffff",
        'light_gray': "#ecf0f1",
        'dark_bg': "#2c3e50",
        'error_color': "#e74c3c",
        'warning_color': "#f39c12",
        
        # Button colors
        'button_accent': "#3498db",
        'button_accent_hover': "#2980b9",
        'button_accent_pressed': "#21618c",
        'button_modern': "#34495e",
        'button_modern_hover': "#2c3e50",
        'button_warning': "#f39c12",
        'button_warning_hover': "#e67e22",
        'button_red': "#e74c3c",
        'button_red_hover': "#c0392b",
        
        # Editor colors
        'editor_bg': "#ffffff",
        'editor_fg': "#2c3e50",
        'editor_select_bg': "#3498db",
        'editor_select_fg': "white",
        'editor_cursor': "#2c3e50",
        
        # Console/Results colors (Dark theme)
        'console_bg': "#1e1e1e",
        'console_fg': "#ffffff",
        'console_select_bg': "#264f78",
        'console_select_fg': "white",
        
        # Treeview colors
        'treeview_heading_bg': "#34495e",
        'treeview_heading_fg': "white",
        'treeview_bg': "white",
        'treeview_fg': "#2c3e50",
        
        # Progressbar colors
        'progress_trough': "#ecf0f1",
        'progress_bar': "#3498db",
    }
    
    # =============================================================================
    # FONT DEFINITIONS
    # =============================================================================
    
    FONTS = {
        'normal': ('Segoe UI', 11),
        'bold': ('Segoe UI', 11, 'bold'),
        'label': ('Segoe UI', 11, 'bold'),
        'header': ('Segoe UI', 12, 'bold'),
        'database': ('Segoe UI', 12, 'bold'),
        'subtitle': ('Segoe UI', 14, 'bold'),
        'small': ('Segoe UI', 10),
        
        # Special fonts
        'logo_title': ('Segoe UI', 18, 'bold'),
        'logo_subtitle': ('Segoe UI', 12),
        'code': ('Consolas', 12),
        'console': ('Consolas', 11),
        'history': ('Consolas', 11),
    }
    
    # =============================================================================
    # UI LAYOUT SETTINGS
    # =============================================================================
    
    LAYOUT = {
        # Window settings
        'window_state': 'zoomed',
        'fullscreen': True,
        
        # Padding and margins
        'card_padding': (40, 40),
        'container_padding': (12, 12),
        'button_padding': (12, 8),
        'header_padding': 15,
        
        # Component sizes
        'query_editor_height': 20,
        'result_viewer_height': 10,
        'logo_size': (240, 120),
        'logo_fallback_size': (80, 40),
        
        # Paned window weights
        'editor_weight': 7,
        'console_weight': 3,
        'left_panel_weight': 1,
        'right_panel_weight': 3,
        
        # Border settings
        'border_width': 1,
        'highlight_thickness': 1,
        
        # Treeview settings
        'treeview_row_height': 25,
        
        # History dialog
        'history_window_size': "700x500",
        'history_listbox_size': (80, 20),
    }
    
    # =============================================================================
    # QUERY SETTINGS
    # =============================================================================
    
    QUERY = {
        # Dangerous SQL keywords for validation
        'dangerous_keywords': [
            "drop table", "drop database", "truncate table",
            "delete from", "alter table", "update "
        ],
        
        # Query formatting
        'max_preview_length': 50,
        'max_history_preview': 60,
        'query_preview_suffix': "...",
        
        # Execution settings
        'fetch_batch_size': 1000,
        'max_column_width': 50,
    }
    
    # =============================================================================
    # FILE SETTINGS
    # =============================================================================
    
    FILES = {
        # Log file settings
        'log_extension': '.log',
        'log_encoding': 'utf-8',
        'log_filetypes': [
            ("Log Files", "*.log"), 
            ("Text Files", "*.txt"), 
            ("All Files", "*.*")
        ],
        
        # Assets
        'logo_path': os.path.join("assets", "logo.png"),
        'icon_path': os.path.join("assets", "logo.png"),
    }
    
    # =============================================================================
    # UI TEXT AND MESSAGES
    # =============================================================================
    
    MESSAGES = {
        # Connection messages
        'connect_success': "Connected successfully",
        'connect_error': "Connection failed",
        'connecting': "Connecting...",
        'not_connected': "Not connected",
        
        # Query messages
        'query_running': "Query already running",
        'no_databases': "Select at least one database.",
        'no_query': "Enter a SQL query.",
        'dangerous_query': "⚠️ This query may modify or delete data.\n\nDo you want to proceed?",
        'query_executing': "Executing query...",
        'query_completed': "Query execution completed",
        'query_failed': "Query execution failed",
        
        # History messages
        'no_history': "No query history yet.",
        'no_results_to_save': "No query results to save",
        
        # Validation messages
        'server_required': "Server is required",
        'username_required': "Username is required",
        
        # UI Labels
        'company_name': "Zanvar Group of Industries",
        'login_subtitle': "Login to your database",
        'select_all_databases': "Select All Databases",
        'available_databases': "Available Databases:",
        'query_editor_title': "💻 Query Editor (Ctrl+Enter to execute, Ctrl+A to select all)",
        'results_title': "📊 Query Results & Output Console",
        'query_history_title': "📜 Query History",
        'history_instruction': "Double-click to load a query",
        
        # Button texts
        'connect_button': "Connect",
        'disconnect_button': "Disconnect",
        'exit_button': "Exit",
        'execute_button': "▶️ Execute Query",
        'history_button': "📜 History",
        'clear_editor_button': "🧹 Clear Editor",
        'export_button': "💾 Export Results",
        'clear_results_button': "🧹 Clear Results",
    }
    
    # =============================================================================
    # KEYBOARD SHORTCUTS
    # =============================================================================
    
    SHORTCUTS = {
        'execute_query': '<Control-Return>',
        'select_all': '<Control-a>',
    }
    
    # =============================================================================
    # VALIDATION RULES
    # =============================================================================
    
    VALIDATION = {
        'min_server_length': 1,
        'min_username_length': 1,
        'max_query_preview': 47,
        'max_filename_hash_length': 8,
    }
    
    # =============================================================================
    # THREADING SETTINGS
    # =============================================================================
    
    THREADING = {
        'queue_check_interval': 100,  # milliseconds
        'daemon_threads': True,
        'connection_switch_delay': 1000,  # milliseconds
    }
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    @classmethod
    def get_logo_path(cls):
        """Get the full path to the logo file"""
        return cls.FILES['logo_path']
    
    @classmethod
    def get_dangerous_keywords(cls):
        """Get list of dangerous SQL keywords"""
        return cls.QUERY['dangerous_keywords']
    
    @classmethod
    def get_default_connection(cls):
        """Get default connection settings"""
        return {
            'server': cls.DEFAULT_SERVER,
            'username': cls.DEFAULT_USERNAME,
            'password': cls.DEFAULT_PASSWORD
        }
    
    @classmethod
    def get_window_config(cls):
        """Get window configuration settings"""
        return {
            'title': cls.APP_TITLE,
            'geometry': cls.APP_GEOMETRY,
            'state': cls.LAYOUT['window_state'],
            'fullscreen': cls.LAYOUT['fullscreen'],
            'bg': cls.COLORS['bg_color']
        }
    
    @classmethod
    def get_editor_config(cls):
        """Get query editor configuration"""
        return {
            'height': cls.LAYOUT['query_editor_height'],
            'font': cls.FONTS['code'],
            'bg': cls.COLORS['editor_bg'],
            'fg': cls.COLORS['editor_fg'],
            'selectbackground': cls.COLORS['editor_select_bg'],
            'selectforeground': cls.COLORS['editor_select_fg'],
            'insertbackground': cls.COLORS['editor_cursor']
        }
    
    @classmethod
    def get_console_config(cls):
        """Get console/results viewer configuration"""
        return {
            'height': cls.LAYOUT['result_viewer_height'],
            'font': cls.FONTS['console'],
            'bg': cls.COLORS['console_bg'],
            'fg': cls.COLORS['console_fg'],
            'selectbackground': cls.COLORS['console_select_bg'],
            'selectforeground': cls.COLORS['console_select_fg']
        }

# =============================================================================
# ENVIRONMENT-SPECIFIC SETTINGS
# =============================================================================

class DevConfig(AppConfig):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProdConfig(AppConfig):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"

# Default configuration
Config = AppConfig
