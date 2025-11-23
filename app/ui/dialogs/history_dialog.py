import tkinter as tk
from tkinter import ttk, messagebox

class HistoryDialog:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.window = None

    def show_history(self):
        """Show complete query history dialog with modern styling - Complete implementation from original"""
        history = self.app.get_query_history()
        
        if not history:
            messagebox.showinfo("History", "No query history yet.")
            return
            
        # Create the history window
        self.window = tk.Toplevel(self.parent)
        self.window.title("Query History")
        self.window.geometry("700x500")
        self.window.configure(bg=self.app.bg_color)
        
        # Make window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center the window
        self._center_window()
        
        # Build the UI
        self._build_header()
        self._build_history_list(history)
        
        # Focus the window
        self.window.focus_set()

    def _center_window(self):
        """Center the dialog window on parent"""
        self.window.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.window.winfo_reqwidth()
        dialog_height = self.window.winfo_reqheight()
        
        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.window.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def _build_header(self):
        """Build modern header from original code"""
        header_frame = tk.Frame(self.window, bg=self.app.card_bg, pady=15)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        tk.Label(
            header_frame, 
            text="📜 Query History", 
            font=self.app.font_subtitle,
            bg=self.app.card_bg,
            fg=self.app.primary_color
        ).pack(side="left")
        
        tk.Label(
            header_frame, 
            text="Double-click to load a query", 
            font=self.app.font_small,
            bg=self.app.card_bg,
            fg=self.app.muted_color
        ).pack(side="right")

    def _build_history_list(self, history):
        """Build history listbox with modern styling from original code"""
        # History listbox with modern styling
        list_frame = tk.Frame(self.window, bg=self.app.bg_color)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create listbox with scrollbar
        self.listbox = tk.Listbox(
            list_frame, 
            width=80, 
            height=20, 
            font=('Consolas', 11),
            bg=self.app.card_bg,
            fg=self.app.primary_color,
            selectbackground=self.app.accent_color,
            selectforeground="white"
        )
        
        scrollbar = ttk.Scrollbar(list_frame, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate history (reversed to show newest first)
        for dt, q in reversed(history):
            preview = q if len(q) <= 60 else q[:57] + "..."
            self.listbox.insert(tk.END, f"{dt:%Y-%m-%d %H:%M:%S}: {preview}")
        
        # Bind double-click event
        self.listbox.bind("<Double-Button-1>", self._on_double_click)
        
        # Bind keyboard events
        self.listbox.bind("<Return>", self._on_double_click)
        self.listbox.bind("<Escape>", lambda e: self.window.destroy())
        
        # Build button frame
        self._build_buttons()

    def _build_buttons(self):
        """Build button frame with Load and Close buttons"""
        button_frame = tk.Frame(self.window, bg=self.app.bg_color, pady=10)
        button_frame.pack(fill="x", padx=10)
        
        # Load button
        load_btn = ttk.Button(
            button_frame,
            text="Load Query",
            style='Accent.TButton',
            command=self._load_selected_query
        )
        load_btn.pack(side="left", padx=(0, 10))
        
        # Delete button
        delete_btn = ttk.Button(
            button_frame,
            text="Delete Selected",
            style='Warning.TButton',
            command=self._delete_selected_query
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        # Clear all button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear All History",
            style='Red.TButton',
            command=self._clear_all_history
        )
        clear_btn.pack(side="left", padx=(0, 10))
        
        # Close button
        close_btn = ttk.Button(
            button_frame,
            text="Close",
            style='Modern.TButton',
            command=self.window.destroy
        )
        close_btn.pack(side="right")

    def _on_double_click(self, event):
        """Handle double-click on history item - Complete logic from original"""
        self._load_selected_query()

    def _load_selected_query(self):
        """Load selected query into editor - Complete logic from original"""
        selection = self.listbox.curselection()
        if selection:
            history = self.app.get_query_history()
            selected_index = selection[0]
            
            # Get the query (remember history is reversed in display)
            _, query = history[-(selected_index + 1)]
            
            # Load query into editor through app controller
            self.app.load_query_from_history(query)
            
            # Close the dialog
            self.window.destroy()

    def _delete_selected_query(self):
        """Delete selected query from history"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a query to delete.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected query from history?"):
            selected_index = selection[0]
            history = self.app.get_query_history()
            
            # Remove from history (remember history is reversed in display)
            actual_index = len(history) - 1 - selected_index
            history.pop(actual_index)
            
            # Save updated history
            self.app.history_manager.save_history()
            
            # Refresh the list
            self._refresh_history_list()

    def _clear_all_history(self):
        """Clear all query history"""
        if messagebox.askyesno("Confirm Clear All", "Are you sure you want to clear all query history?"):
            self.app.history_manager.clear_history()
            self._refresh_history_list()

    def _refresh_history_list(self):
        """Refresh the history list display"""
        # Clear current list
        self.listbox.delete(0, tk.END)
        
        # Repopulate with updated history
        history = self.app.get_query_history()
        if history:
            for dt, q in reversed(history):
                preview = q if len(q) <= 60 else q[:57] + "..."
                self.listbox.insert(tk.END, f"{dt:%Y-%m-%d %H:%M:%S}: {preview}")
        else:
            # Close dialog if no history left
            messagebox.showinfo("History Cleared", "All query history has been cleared.")
            self.window.destroy()

    def _get_selected_query_info(self):
        """Get information about the selected query"""
        selection = self.listbox.curselection()
        if selection:
            history = self.app.get_query_history()
            selected_index = selection[0]
            actual_index = len(history) - 1 - selected_index
            
            dt, query = history[actual_index]
            return {
                'datetime': dt,
                'query': query,
                'index': actual_index,
                'preview': query if len(query) <= 60 else query[:57] + "..."
            }
        return None
