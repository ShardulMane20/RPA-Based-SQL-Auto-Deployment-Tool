import tkinter as tk
from tkinter import scrolledtext

class QueryEditor:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.query_text = None
        self.query_editor_frame = None
        self.build_editor()

    def build_editor(self):
        """Build query editor component - Complete implementation from original build_query_view"""
        # Query editor with modern styling - Made larger
        self.query_editor_frame = tk.Frame(
            self.parent, 
            bg=self.app.card_bg, 
            relief="solid", 
            bd=1,
            highlightbackground=self.app.border_color, 
            highlightthickness=1
        )
        
        query_editor_container = tk.Frame(
            self.query_editor_frame, 
            bg=self.app.card_bg, 
            padx=12, 
            pady=12
        )
        query_editor_container.pack(fill="both", expand=True)
        
        # Editor header
        editor_header = tk.Frame(
            query_editor_container, 
            bg=self.app.light_gray, 
            relief="solid", 
            bd=1
        )
        editor_header.pack(fill="x", pady=(0, 8))
        
        editor_title = tk.Label(
            editor_header,
            text="💻 Query Editor (Ctrl+Enter to execute)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.app.light_gray,
            fg=self.app.primary_color,
            pady=8
        )
        editor_title.pack(anchor="w", padx=12)
        
        # Query text area with modern styling
        self.query_text = scrolledtext.ScrolledText(
            query_editor_container, 
            wrap=tk.NONE, 
            height=20,  # Increased height
            font=('Consolas', 12),
            undo=True, 
            maxundo=100,
            bg="#ffffff",
            fg="#2c3e50",
            selectbackground="#3498db",
            selectforeground="white",
            insertbackground="#2c3e50",
            relief="solid",
            bd=1,
            highlightbackground=self.app.border_color,
            highlightthickness=1,
            padx=8,
            pady=8
        )
        self.query_text.pack(fill="both", expand=True)
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()

    def bind_shortcuts(self):
        """Bind keyboard shortcuts from original"""
        # Ctrl+Enter to execute query
        self.query_text.bind("<Control-Return>", lambda e: self._execute_query())
        
        # Additional useful shortcuts
        self.query_text.bind("<Control-a>", self._select_all)
        self.query_text.bind("<Control-A>", self._select_all)

    def _execute_query(self):
        """Execute query through app controller"""
        # Get selected databases and query text
        selected_databases = self.app.main_ui.get_selected_databases() if hasattr(self.app, 'main_ui') else []
        query = self.get_query()
        
        # Execute through app controller
        self.app.start_query_thread(selected_databases, query)

    def _select_all(self, event):
        """Select all text in the editor"""
        self.query_text.tag_add(tk.SEL, "1.0", tk.END)
        self.query_text.mark_set(tk.INSERT, "1.0")
        self.query_text.see(tk.INSERT)
        return 'break'  # Prevent default behavior

    def get_query(self):
        """Get current query text"""
        return self.query_text.get("1.0", tk.END).strip()

    def clear_editor(self):
        """Clear editor content"""
        self.query_text.delete("1.0", tk.END)

    def set_query(self, query):
        """Set query text"""
        self.query_text.delete("1.0", tk.END)
        self.query_text.insert(tk.END, query)

    def get_frame(self):
        """Return the main frame for packing"""
        return self.query_editor_frame

    def enable(self):
        """Enable the query editor"""
        self.query_text.config(state="normal")

    def disable(self):
        """Disable the query editor"""
        self.query_text.config(state="disabled")

    def is_empty(self):
        """Check if editor is empty"""
        content = self.get_query()
        return len(content) == 0

    def insert_text(self, text, position=None):
        """Insert text at specified position or current cursor position"""
        if position is None:
            position = self.query_text.index(tk.INSERT)
        self.query_text.insert(position, text)

    def replace_text(self, start, end, new_text):
        """Replace text in specified range"""
        self.query_text.delete(start, end)
        self.query_text.insert(start, new_text)

    def get_selected_text(self):
        """Get currently selected text"""
        try:
            return self.query_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return ""

    def has_selection(self):
        """Check if there is any text selected"""
        try:
            self.query_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            return True
        except tk.TclError:
            return False

    def focus(self):
        """Set focus to the query editor"""
        self.query_text.focus_set()

    def undo(self):
        """Undo last operation"""
        try:
            self.query_text.edit_undo()
        except tk.TclError:
            pass  # Nothing to undo

    def redo(self):
        """Redo last operation"""
        try:
            self.query_text.edit_redo()
        except tk.TclError:
            pass  # Nothing to redo

    def find_text(self, search_text, start="1.0"):
        """Find text in the editor"""
        pos = self.query_text.search(search_text, start, tk.END)
        if pos:
            end_pos = f"{pos}+{len(search_text)}c"
            self.query_text.tag_remove(tk.SEL, "1.0", tk.END)
            self.query_text.tag_add(tk.SEL, pos, end_pos)
            self.query_text.mark_set(tk.INSERT, end_pos)
            self.query_text.see(pos)
            return pos
        return None

    def get_cursor_position(self):
        """Get current cursor position"""
        return self.query_text.index(tk.INSERT)

    def set_cursor_position(self, position):
        """Set cursor position"""
        self.query_text.mark_set(tk.INSERT, position)
        self.query_text.see(position)

    def get_line_count(self):
        """Get number of lines in the editor"""
        return int(self.query_text.index(tk.END).split('.')[0]) - 1

    def get_text_stats(self):
        """Get text statistics"""
        text = self.get_query()
        return {
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '')),
            'words': len(text.split()),
            'lines': self.get_line_count(),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
        }
