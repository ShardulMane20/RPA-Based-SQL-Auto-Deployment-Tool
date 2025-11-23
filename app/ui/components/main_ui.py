# A small description for the code file.
# This file defines the main user interface after a successful connection.
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .database_explorer import DatabaseExplorer
from .query_editor import QueryEditor
from .result_viewer import ResultViewer
from datetime import datetime
import hashlib

class MainUI:
    def __init__(self, root, app_controller):
        self.root = root
        self.app = app_controller
        self.main_frame = None
        
        # UI components
        self.database_explorer = None
        self.query_editor = None
        self.result_viewer = None
        
        # UI elements
        self.run_query_btn = None
        self.save_log_btn = None
        
        # Connection status elements
        self.connection_status_frame = None
        self.server_label = None
        self.username_label = None
        
        self.build_ui()

    def build_ui(self):
        """Build main application UI - Complete implementation from original build_main_ui"""
        if hasattr(self, 'main_frame') and self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg=self.app.bg_color)
        
        # Modern header with all buttons
        self.build_main_ui_header()

        # Main content with paned window
        paned = ttk.PanedWindow(self.main_frame, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create left and right panels
        left_panel = ttk.Frame(paned, padding=10)
        right_panel = ttk.Frame(paned, padding=10)

        # FIXED: Removed minsize parameter - ttk.PanedWindow doesn't support it
        # Make left panel much narrower (weight=1) and right panel wider (weight=39)
        # This creates approximately 2.5% left and 97.5% right split
        paned.add(left_panel, weight=1)
        paned.add(right_panel, weight=39)
        
        # Build components
        self.build_database_explorer(left_panel)
        self.build_query_view(right_panel)

    def build_main_ui_header(self):
        """Build modern header with connection status and all action buttons - Complete from original"""
        header_frame = tk.Frame(
            self.main_frame, 
            bg=self.app.card_bg, 
            pady=15,
            highlightbackground="#e0e0e0",
            highlightthickness=1
        )
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)  # Make middle column expandable
        
        # Left side - Connection status
        self._build_connection_status(header_frame)
        
        # Center - Action buttons (moved from query view)
        self._build_action_buttons(header_frame)
        
        # Right side - Disconnect button
        ttk.Button(
            header_frame, 
            text="Disconnect", 
            style='Red.TButton', 
            command=self.app.disconnect_server
        ).grid(row=0, column=2, sticky="e", padx=10)

    def _build_connection_status(self, parent):
        """Build connection status display - FIXED VERSION"""
        # Clear existing connection status frame if it exists
        if hasattr(self, 'connection_status_frame') and self.connection_status_frame:
            self.connection_status_frame.destroy()
        
        self.connection_status_frame = tk.Frame(parent, bg=self.app.card_bg)
        self.connection_status_frame.grid(row=0, column=0, sticky="w", padx=10)
        
        # Try to get server info from app controller
        try:
            # Check if the app controller has connection info stored
            if hasattr(self.app, 'current_server_info') and self.app.current_server_info:
                server_info = self.app.current_server_info
            elif hasattr(self.app, 'connection_details') and self.app.connection_details:
                server_info = self.app.connection_details
            elif hasattr(self.app, 'server') and hasattr(self.app, 'username'):
                server_info = {
                    'server': self.app.server,
                    'username': self.app.username
                }
            else:
                # Fallback: try to get from connection UI if available
                if hasattr(self.app, 'connection_ui') and self.app.connection_ui:
                    details = self.app.connection_ui.get_connection_details()
                    if details and details.get('server') and details.get('username'):
                        server_info = details
                    else:
                        server_info = None
                else:
                    server_info = None
            
            if server_info and server_info.get('server') and server_info.get('username'):
                # Connected status with proper labels
                tk.Label(
                    self.connection_status_frame, 
                    text="🟢 Connected to: ", 
                    bg=self.app.card_bg,
                    fg=self.app.success_color,
                    font=self.app.font_normal
                ).pack(side="left", anchor="center")
                
                self.username_label = tk.Label(
                    self.connection_status_frame, 
                    text=f"{server_info.get('username', 'Unknown')} ", 
                    bg=self.app.card_bg,
                    fg=self.app.primary_color,
                    font=('Segoe UI', 10, 'bold')
                )
                self.username_label.pack(side="left", anchor="center")
                
                tk.Label(
                    self.connection_status_frame, 
                    text="on ", 
                    bg=self.app.card_bg,
                    fg=self.app.primary_color,
                    font=self.app.font_normal
                ).pack(side="left", anchor="center")
                
                self.server_label = tk.Label(
                    self.connection_status_frame, 
                    text=server_info.get('server', 'Unknown'),
                    bg=self.app.card_bg,
                    fg=self.app.primary_color,
                    font=('Segoe UI', 10, 'bold')
                )
                self.server_label.pack(side="left", anchor="center")
            else:
                # Fallback status if connection info is not available
                tk.Label(
                    self.connection_status_frame, 
                    text="🟡 Connection Status Unknown", 
                    bg=self.app.card_bg,
                    fg=self.app.muted_color,
                    font=self.app.font_normal
                ).pack(side="left", anchor="center")
                
        except Exception as e:
            # Error handling - show error status
            tk.Label(
                self.connection_status_frame, 
                text="🔴 Connection Status Error", 
                bg=self.app.card_bg,
                fg=self.app.error_color,
                font=self.app.font_normal
            ).pack(side="left", anchor="center")

    def _build_action_buttons(self, parent):
        """Build center action buttons"""
        button_frame = tk.Frame(parent, bg=self.app.card_bg)
        button_frame.grid(row=0, column=1, sticky="", padx=20)
        
        self.run_query_btn = ttk.Button(
            button_frame, 
            text="▶️ Execute Query", 
            style='Accent.TButton', 
            command=self._execute_query
        )
        self.run_query_btn.grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame, 
            text="📜 History", 
            style='Modern.TButton',
            command=self.app.show_query_history
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame, 
            text="🧹 Clear Editor", 
            style='Warning.TButton',
            command=self.clear_query_editor
        ).grid(row=0, column=2, padx=5)

        self.save_log_btn = ttk.Button(
            button_frame, 
            text="💾 Export Results", 
            style='Modern.TButton',
            command=self._export_results,
            state='disabled'
        )
        self.save_log_btn.grid(row=0, column=3, padx=5)

        ttk.Button(
            button_frame, 
            text="🧹 Clear Results", 
            style='Warning.TButton',
            command=self.clear_results
        ).grid(row=0, column=4, padx=5)

    def build_database_explorer(self, parent):
        """Build database explorer component"""
        self.database_explorer = DatabaseExplorer(parent, self.app)

    def build_query_view(self, parent):
        """Build query editor and result viewer - Complete implementation from original"""
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Query pane with adjusted weights
        query_pane = ttk.PanedWindow(parent, orient="vertical")
        query_pane.grid(row=0, column=0, sticky="nsew")

        # Query editor
        self.query_editor = QueryEditor(query_pane, self.app)

        # Result viewer
        self.result_viewer = ResultViewer(query_pane, self.app)

        # Adjusted weights for the vertical panels
        # The query editor is now larger and the result viewer is smaller.
        # Total parts = 8 + 2 = 10. Editor gets 8/10 (80%), results get 2/10 (20%).
        query_pane.add(self.query_editor.get_frame(), weight=8)
        query_pane.add(self.result_viewer.get_frame(), weight=2)

    def _execute_query(self):
        """Execute query through app controller"""
        selected_databases = self.database_explorer.get_selected_databases()
        query = self.query_editor.get_query()
        self.app.start_query_thread(selected_databases, query)

    def _export_results(self):
        """Export current results to file"""
        try:
            # Check if there are results to export
            if self.result_viewer.is_empty():
                messagebox.showwarning("No Results", "No query results to export. Please execute a query first.")
                return
            
            # Get current results content
            results_content = self.result_viewer.get_results_content()
            
            if not results_content:
                messagebox.showwarning("No Results", "No query results to export.")
                return
            
            # Get current query for filename generation
            current_query = self.query_editor.get_query().strip() if self.query_editor else ""
            
            # Generate default filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if current_query:
                query_hash = hashlib.md5(current_query.encode()).hexdigest()[:8]
                default_filename = f"SQLResults_{timestamp}_{query_hash}.log"
            else:
                default_filename = f"SQLResults_{timestamp}.log"
            
            # Ask user for save location
            filepath = filedialog.asksaveasfilename(
                initialfile=default_filename,
                defaultextension=".log",
                filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Export Query Results"
            )
            
            if not filepath:
                return
            
            # Create export content with header
            server_info = self.app.get_current_server_info()
            export_content = f"SQL Tool Query Results Export\n"
            export_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            if server_info:
                export_content += f"Server: {server_info.get('server', 'Unknown')}\n"
                export_content += f"User: {server_info.get('username', 'Unknown')}\n"
            
            if current_query:
                export_content += f"\nQuery:\n{current_query}\n"
            
            export_content += f"\n{'='*80}\n"
            export_content += f"RESULTS:\n\n{results_content}\n"
            export_content += f"\n{'='*80}\n"
            export_content += f"Export completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            # Save the file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            messagebox.showinfo("Export Successful", f"Results exported successfully to:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export results:\n{str(e)}")

    # --- Methods below are for state management and delegation ---
    
    def set_query_running_state(self, is_running):
        """Set UI state based on query execution status"""
        state = "disabled" if is_running else "normal"
        self.run_query_btn.config(state=state)
        if is_running:
            self.save_log_btn.config(state="disabled")
            self.query_editor.disable()
        else:
            self.query_editor.enable()

    def enable_save_log_button(self):
        """Enable the save log button"""
        self.save_log_btn.config(state="normal")

    def populate_databases(self, databases):
        """Populate databases in explorer"""
        if self.database_explorer:
            self.database_explorer.populate_databases(databases)

    def clear_query_editor(self):
        """Clear the query editor"""
        if self.query_editor:
            self.query_editor.clear_editor()

    def set_query_text(self, query):
        """Set query text in editor"""
        if self.query_editor:
            self.query_editor.set_query(query)

    def get_query_text(self):
        """Get query text from editor"""
        if self.query_editor:
            return self.query_editor.get_query()
        return ""

    def clear_results(self):
        """Clear the results viewer"""
        if self.result_viewer:
            self.result_viewer.clear_results()

    def show_execution_summary(self, summary):
        """Display execution summary in results"""
        if self.result_viewer:
            self.result_viewer.show_execution_summary(summary)

    def append_result(self, result):
        """Append result to results viewer"""
        if self.result_viewer:
            self.result_viewer.append_result(result)

    def show_status(self, status):
        """Show status in results viewer"""
        if self.result_viewer:
            self.result_viewer.show_status(status)

    def show_error(self, error_message):
        """Show error in results viewer"""
        if self.result_viewer:
            self.result_viewer.show_error(error_message)

    def show(self):
        """Show main UI"""
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide main UI"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def get_selected_databases(self):
        """Get selected databases from explorer"""
        if self.database_explorer:
            return self.database_explorer.get_selected_databases()
        return []

    def has_database_selection(self):
        """Check if any databases are selected"""
        if self.database_explorer:
            return self.database_explorer.has_selection()
        return False

    def get_database_info(self):
        """Get database information"""
        if self.database_explorer:
            return self.database_explorer.get_database_info()
        return {}

    def refresh_connection_status(self):
        """Refresh connection status display - IMPROVED VERSION"""
        try:
            # Just rebuild the connection status section instead of destroying the entire header
            if hasattr(self, 'connection_status_frame') and self.connection_status_frame:
                # Find the parent of connection_status_frame (should be header_frame)
                header_frame = self.connection_status_frame.master
                if header_frame:
                    self._build_connection_status(header_frame)
        except Exception as e:
            print(f"Error refreshing connection status: {e}")
            # Fallback: rebuild entire header if needed
            try:
                self.build_main_ui_header()
            except Exception as fallback_error:
                print(f"Fallback header rebuild also failed: {fallback_error}")

    def update_connection_info(self, server, username):
        """Update connection info display directly - NEW METHOD"""
        try:
            if hasattr(self, 'server_label') and self.server_label:
                self.server_label.config(text=server)
            if hasattr(self, 'username_label') and self.username_label:
                self.username_label.config(text=f"{username} ")
        except Exception as e:
            print(f"Error updating connection info: {e}")
            # Rebuild the connection status if direct update fails
            self.refresh_connection_status()

    def set_connection_info(self, server_info):
        """Set connection information for display - NEW METHOD"""
        if hasattr(self.app, 'current_server_info'):
            self.app.current_server_info = server_info
        else:
            # Store it directly in app controller
            self.app.connection_details = server_info
        
        # Update the display
        if server_info and server_info.get('server') and server_info.get('username'):
            self.update_connection_info(server_info['server'], server_info['username'])