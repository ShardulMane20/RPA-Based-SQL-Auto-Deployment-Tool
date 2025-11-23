import tkinter as tk
from tkinter import ttk, messagebox
import threading
from queue import Queue, Empty
from datetime import datetime
import os

from app.ui.components.connection_ui import ConnectionUI
from app.ui.components.main_ui import MainUI
from app.ui.styling.styles import StyleManager
from app.ui.styling.logo_handler import LogoHandler
from app.database.connection import DatabaseManager
from app.database.query_executor import QueryExecutor
from app.utils.query_history import QueryHistoryManager
from app.utils.file_operations import FileOperationsManager
from app.utils.validators import QueryValidator
from app.core.config import AppConfig


class SQLToolApp:
    def __init__(self, root):
        self.root = root
        # Initialize basic attributes first
        self.conn = None
        self.current_server = None
        self.current_db = None
        self.db_vars = {}
        self.db_checkbuttons = {}
        self.message_queue = Queue()
        self.query_history = []
        self.query_running = False
        self.current_query = None
        
        # Store connection details for display
        self.connection_details = None
        
        self.setup_application()
        self.initialize_managers()
        self.initialize_ui()
        self.check_queue()  # Start queue checking

    def setup_application(self):
        """Complete application setup logic"""
        self.root.title("Zanvar's SQL Tool")
        # Set login window to specific size (not fullscreen)
        self.root.geometry("1200x800")  # Adjusted size for login window
        self.root.resizable(False, False)  # Prevent resizing for login window
        
        # Set colors and fonts from config
        self.bg_color = AppConfig.COLORS['bg_color']
        self.primary_color = AppConfig.COLORS['primary_color']
        self.muted_color = AppConfig.COLORS['muted_color']
        self.success_color = AppConfig.COLORS['success_color']
        self.accent_color = AppConfig.COLORS['accent_color']
        self.border_color = AppConfig.COLORS['border_color']
        self.card_bg = AppConfig.COLORS['card_bg']
        self.light_gray = AppConfig.COLORS['light_gray']
        self.dark_bg = AppConfig.COLORS['dark_bg']
        self.error_color = AppConfig.COLORS['error_color']
        self.warning_color = AppConfig.COLORS['warning_color']

        # Font definitions
        self.font_normal = AppConfig.FONTS['normal']
        self.font_bold = AppConfig.FONTS['bold']
        self.font_label = AppConfig.FONTS['label']
        self.font_header = AppConfig.FONTS['header']
        self.font_database = AppConfig.FONTS['database']
        self.font_subtitle = AppConfig.FONTS['subtitle']
        self.font_small = AppConfig.FONTS['small']

        # Create logo
        self.logo_image = LogoHandler.create_logo_placeholder()
        
        # Configure root background
        self.root.configure(bg=self.bg_color)

    def initialize_managers(self):
        """Initialize all manager classes"""
        self.style_manager = StyleManager(self.root, self)
        self.db_manager = DatabaseManager()
        self.history_manager = QueryHistoryManager()
        self.query_executor = QueryExecutor(self.db_manager, self.message_queue)
        self.file_manager = FileOperationsManager()
        
    def initialize_ui(self):
        """Initialize UI components"""
        self.connection_ui = ConnectionUI(self.root, self)
        self.main_ui = MainUI(self.root, self)
        self.connection_ui.show()

    # Connection methods
    def connect_to_server(self, server, username, password):
        """Handle server connection request from UI"""
        if not server.strip():
            messagebox.showwarning("Input Error", "Server is required")
            return
        if not username.strip():
            messagebox.showwarning("Input Error", "Username is required")
            return
        
        # Store connection details for later use
        self.connection_details = {
            'server': server,
            'username': username,
            'password': password
        }
            
        self.db_manager.set_server_config(server, username, password)
        self.current_server = self.db_manager.current_server
        
        # Start connection attempt in thread
        threading.Thread(target=self.attempt_connection, daemon=True).start()

    def attempt_connection(self):
        """Attempt to connect to server with better error handling"""
        success, message = self.db_manager.test_connection()
        
        if success:
            self.message_queue.put(("success", message))
        else:
            self.message_queue.put(("error", f"Connection failed: {message}"))

    def disconnect_server(self):
        """Disconnect from the current server"""
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
            finally:
                self.conn = None
                
        self.current_server = None
        self.connection_details = None
        self.db_vars = {}
        
        # Switch back to connection UI and restore login window size
        self.main_ui.hide()
        self.root.attributes('-fullscreen', False)
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.connection_ui.show()

    # Query execution methods
    def start_query_thread(self, selected_databases, query):
        """Start a new thread to execute the query"""
        if self.query_running:
            messagebox.showwarning("Wait", "Query already running")
            return
            
        if not selected_databases:
            messagebox.showwarning("Selection Error", "Select at least one database.")
            return
            
        if not query.strip():
            messagebox.showwarning("Input Error", "Enter a SQL query.")
            return

        # Validate query for dangerous operations
        if QueryValidator.contains_dangerous_sql(query):
            confirm = messagebox.askyesno(
                "Confirm Destructive Query",
                "⚠️ This query may modify or delete data.\n\nDo you want to proceed?"
            )
            if not confirm:
                return

        # Store current query details for logging
        self.current_query = {
            'query': query,
            'databases': selected_databases,
            'start_time': datetime.now(),
            'results': []
        }

        # Add to history
        self.history_manager.add_query(query)
        
        # Update UI state
        self.query_running = True
        self.main_ui.set_query_running_state(True)
        self.main_ui.clear_results()
        self.main_ui.show_status("Executing query...")
        
        # Start execution thread
        threading.Thread(
            target=self._execute_query_thread, 
            args=(selected_databases, query), 
            daemon=True
        ).start()

    def _execute_query_thread(self, databases, query):
        """Execute query in separate thread"""
        try:
            result = self.query_executor.execute_query(databases, query)
            self.current_query.update(result)
            self.message_queue.put(("done", "Query execution completed"))
            self.message_queue.put(("enable_log_button", True))
        except Exception as e:
            self.message_queue.put(("error", f"Query execution failed: {str(e)}"))
            self.message_queue.put(("done", "Query execution failed"))

    # File operations
    def save_query_log(self):
        """Save the current query and results to a log file"""
        if not hasattr(self, 'current_query') or not self.current_query.get('results'):
            messagebox.showwarning("No Results", "No query results to save")
            return
        
        success, message = self.file_manager.save_query_log(self.current_query, self.current_server)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def show_query_history(self):
        """Show query history dialog"""
        from app.ui.dialogs.history_dialog import HistoryDialog
        history_dialog = HistoryDialog(self.root, self)
        history_dialog.show_history()

    def load_query_from_history(self, query):
        """Load query from history into editor"""
        self.main_ui.set_query_text(query)

    # Queue message handling
    def check_queue(self):
        """Check the message queue for updates"""
        try:
            while True:
                msg_type, msg = self.message_queue.get_nowait()

                if msg_type == "enable_log_button":
                    self.main_ui.enable_save_log_button()
                elif msg_type == "success":
                    self.handle_success_message(msg)
                elif msg_type == "error":
                    self.handle_error_message(msg)
                elif msg_type == "execution_summary":
                    self.main_ui.show_execution_summary(msg)
                elif msg_type == "result":
                    self.main_ui.append_result(msg)
                elif msg_type == "status":
                    self.main_ui.show_status(msg)
                elif msg_type == "done":
                    self.query_running = False
                    self.main_ui.set_query_running_state(False)

        except Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def handle_success_message(self, msg):
        """Handle successful connection message"""
        self.connection_ui.show_success(msg)
        # Switch to main UI after successful connection
        self.root.after(1000, self._switch_to_main_ui)

    def handle_error_message(self, msg):
        """Handle error messages"""
        if self.query_running:
            self.main_ui.show_error(msg)
        else:
            self.connection_ui.show_error(msg)

    def _switch_to_main_ui(self):
        """Switch from connection UI to main UI with maximized window (not fullscreen)"""
        try:
            databases = self.db_manager.get_databases()
            self.connection_ui.hide()

            # Set main window to maximized, not fullscreen
            self.root.geometry("")  
            self.root.state('zoomed')
            self.root.attributes('-fullscreen', False)  # disable fullscreen
            self.root.resizable(True, True)  # Allow resizing for main window

            # Pass connection details to main UI
            if self.connection_details:
                self.main_ui.set_connection_info(self.connection_details)

            self.main_ui.populate_databases(databases)
            self.main_ui.show()
        except Exception as e:
            self.handle_error_message(f"Failed to load databases: {str(e)}")

    # Application lifecycle
    def on_close(self):
        """Handle application close event"""
        self.history_manager.save_history()
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        self.root.destroy()

    # Utility methods for UI components
    def get_current_server_info(self):
        """Get current server information for display"""
        return self.connection_details

    def get_query_history(self):
        """Get query history for history dialog"""
        return self.history_manager.get_history()

    def clear_query_editor(self):
        """Clear the query editor"""
        self.main_ui.clear_query_editor()

    def clear_results(self):
        """Clear the results viewer"""
        self.main_ui.clear_results()