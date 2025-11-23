import tkinter as tk
from tkinter import ttk, messagebox

class DatabaseExplorer:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.db_vars = {}
        self.db_checkbuttons = {}
        self.select_all_var = tk.BooleanVar()
        self.db_vars_frame = None
        self.canvas = None
        self.scrollbar = None
        self.select_all_cb = None
        self.build_explorer()

    def build_explorer(self):
        """Build complete database explorer UI - Complete implementation from original build_db_explorer"""
        cf = tk.Frame(self.parent, bg=self.app.bg_color)
        cf.pack(fill="both", expand=True, pady=10)
        
        # Select All section
        self._build_select_all_section(cf)
        
        # Available Databases label
        tk.Label(
            cf, 
            text="Available Databases:", 
            bg=self.app.bg_color,
            fg=self.app.primary_color,
            font=self.app.font_header
        ).pack(anchor="w", pady=(5, 5))
        
        # Database checkboxes with scrolling
        self._build_scrollable_database_list(cf)

    def _build_select_all_section(self, parent):
        """Build select all checkbox section"""
        select_all_frame = tk.Frame(parent, bg=self.app.bg_color)
        select_all_frame.pack(fill="x", pady=(0, 5))
        
        self.select_all_cb = tk.Label(
            select_all_frame, 
            text="☐ Select All Databases",
            font=self.app.font_database,
            bg=self.app.bg_color,
            fg=self.app.primary_color,
            cursor="hand2"
        )
        self.select_all_cb.pack(side="left")
        
        # Bind click event for select all
        self.select_all_cb.bind("<Button-1>", self._on_select_all_click)

    def _build_scrollable_database_list(self, parent):
        """Build scrollable database list with canvas and scrollbar"""
        # Create a frame to hold canvas and scrollbar
        scroll_frame = tk.Frame(parent, bg=self.app.bg_color)
        scroll_frame.pack(fill="both", expand=True)
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_rowconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(scroll_frame, bg=self.app.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.canvas.yview)
        self.db_vars_frame = tk.Frame(self.canvas, bg=self.app.bg_color)
        
        # Configure scrolling
        self.db_vars_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.db_vars_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Place canvas and scrollbar using grid
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Set minimum width for the scrollbar column to ensure visibility
        scroll_frame.grid_columnconfigure(1, minsize=20)  # Ensure scrollbar column has minimum width
        
        # Bind mousewheel to canvas
        self._bind_mousewheel()

    def _bind_mousewheel(self):
        """Bind mousewheel scrolling to canvas"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind to canvas and frame
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.db_vars_frame.bind("<MouseWheel>", _on_mousewheel)

    def _on_select_all_click(self, event):
        """Handle select all checkbox click"""
        self.select_all_var.set(not self.select_all_var.get())
        self.toggle_select_all()
        self.update_select_all_symbol()

    def populate_databases(self, databases):
        """Populate database list - Complete implementation from original"""
        # Clear existing databases
        self.clear_databases()
        
        # Create checkbox for each database
        for db in databases:
            self.create_db_checkbox(db)
        
        # Update canvas scroll region
        if self.canvas:
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_db_checkbox(self, db_name):
        """Create a custom checkbox for database selection - Complete implementation from original"""
        var = tk.BooleanVar()
        cb = tk.Label(
            self.db_vars_frame, 
            text=f"☐ {db_name}",
            font=self.app.font_database,
            bg=self.app.bg_color,
            fg=self.app.primary_color,
            cursor="hand2"
        )
        cb.pack(anchor="w", padx=8, pady=5)
        
        # Bind click event
        cb.bind("<Button-1>", lambda e, d=db_name: self._on_database_click(var, d))
        
        # Store references
        self.db_vars[db_name] = var
        self.db_checkbuttons[db_name] = cb

    def _on_database_click(self, var, db_name):
        """Handle individual database checkbox click"""
        var.set(not var.get())
        self.update_checkbox_symbol(var, db_name)
        self.update_select_all_state()

    def update_checkbox_symbol(self, var, db_name):
        """Update checkbox symbol based on its state - Complete implementation from original"""
        cb = self.db_checkbuttons[db_name]
        if var.get():
            cb.configure(text=f"✔ {db_name}")
        else:
            cb.configure(text=f"☐ {db_name}")

    def update_select_all_symbol(self):
        """Update Select All checkbox symbol based on its state - Complete implementation from original"""
        if self.select_all_var.get():
            self.select_all_cb.configure(text="✔ Select All Databases")
        else:
            self.select_all_cb.configure(text="☐ Select All Databases")

    def toggle_select_all(self):
        """Toggle selection of all databases - Complete implementation from original"""
        select_all = self.select_all_var.get()
        for var in self.db_vars.values():
            var.set(select_all)
        for db in self.db_vars.keys():
            self.update_checkbox_symbol(self.db_vars[db], db)

    def update_select_all_state(self):
        """Update select all checkbox based on individual checkbox states"""
        if not self.db_vars:
            return
        
        selected_count = sum(1 for var in self.db_vars.values() if var.get())
        total_count = len(self.db_vars)
        
        if selected_count == 0:
            self.select_all_var.set(False)
            self.select_all_cb.configure(text="☐ Select All Databases")
        elif selected_count == total_count:
            self.select_all_var.set(True)
            self.select_all_cb.configure(text="✔ Select All Databases")
        else:
            self.select_all_var.set(False)
            self.select_all_cb.configure(text="☐ Select All Databases")

    def get_selected_databases(self):
        """Return list of selected databases"""
        return [db for db, var in self.db_vars.items() if var.get()]

    def clear_databases(self):
        """Clear all database checkboxes"""
        # Clear references
        self.db_vars.clear()
        self.db_checkbuttons.clear()
        
        # Clear UI elements
        if self.db_vars_frame:
            for widget in self.db_vars_frame.winfo_children():
                widget.destroy()
        
        # Reset select all
        self.select_all_var.set(False)
        if self.select_all_cb:
            self.select_all_cb.configure(text="☐ Select All Databases")

    def select_databases(self, database_names):
        """Select specific databases programmatically"""
        for db_name in database_names:
            if db_name in self.db_vars:
                self.db_vars[db_name].set(True)
                self.update_checkbox_symbol(self.db_vars[db_name], db_name)
        self.update_select_all_state()

    def deselect_all_databases(self):
        """Deselect all databases"""
        self.select_all_var.set(False)
        self.toggle_select_all()
        self.update_select_all_symbol()

    def get_database_count(self):
        """Get total number of databases"""
        return len(self.db_vars)

    def get_selected_count(self):
        """Get number of selected databases"""
        return len(self.get_selected_databases())

    def has_databases(self):
        """Check if any databases are available"""
        return len(self.db_vars) > 0

    def has_selection(self):
        """Check if any databases are selected"""
        return self.get_selected_count() > 0

    def get_database_info(self):
        """Get information about databases and selection"""
        return {
            'total_databases': self.get_database_count(),
            'selected_databases': self.get_selected_databases(),
            'selected_count': self.get_selected_count(),
            'all_databases': list(self.db_vars.keys())
        }