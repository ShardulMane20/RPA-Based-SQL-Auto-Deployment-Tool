import tkinter as tk
from tkinter import scrolledtext

class ResultViewer:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.result_text = None
        self.result_viewer_frame = None
        self.build_viewer()

    def build_viewer(self):
        """Build result viewer with dark theme from original code"""
        # Result viewer frame with dark theme - Made smaller
        self.result_viewer_frame = tk.Frame(
            self.parent, 
            bg=self.app.card_bg, 
            relief="solid", 
            bd=1,
            highlightbackground=self.app.border_color, 
            highlightthickness=1
        )
        
        result_viewer_container = tk.Frame(
            self.result_viewer_frame, 
            bg=self.app.card_bg, 
            padx=12, 
            pady=12
        )
        result_viewer_container.pack(fill="both", expand=True)
        
        # Results header with dark theme
        results_header = tk.Frame(
            result_viewer_container, 
            bg=self.app.dark_bg, 
            relief="solid", 
            bd=1
        )
        results_header.pack(fill="x", pady=(0, 8))
        
        results_title = tk.Label(
            results_header,
            text="Query Results & Output Console",
            font=('Segoe UI', 11, 'bold'),
            bg=self.app.dark_bg,
            fg="white",
            pady=8
        )
        results_title.pack(anchor="w", padx=12)
        
        # Result text area with dark theme
        self.result_text = scrolledtext.ScrolledText(
            result_viewer_container, 
            wrap=tk.NONE, 
            height=10,  # Reduced height
            font=('Consolas', 11),
            bg="#1e1e1e",
            fg="#ffffff",
            selectbackground="#264f78",
            selectforeground="white",
            relief="solid",
            bd=1,
            highlightbackground=self.app.border_color,
            highlightthickness=1,
            state="disabled",
            padx=8,
            pady=8
        )
        self.result_text.pack(fill="both", expand=True)

    def clear_results(self):
        """Clear the results text area"""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

    def append_result(self, result):
        """Append result to display"""
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, result)
        self.result_text.config(state="disabled")
        # Auto-scroll to bottom to show latest results
        self.result_text.see(tk.END)

    def show_execution_summary(self, summary):
        """Display the detailed execution summary at the top (from original)"""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)  # Clear previous content
        self.result_text.insert(tk.END, summary + "\n")
        self.result_text.config(state="disabled")
        self.result_text.see("1.0")  # Scroll to top to show summary

    def show_status(self, status_message):
        """Show status message in results area"""
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, f"{status_message}\n")
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def show_error(self, error_message):
        """Show error message in results area"""
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, f"ERROR: {error_message}\n")
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def get_frame(self):
        """Return the main frame for packing"""
        return self.result_viewer_frame

    def is_empty(self):
        """Check if result viewer is empty"""
        content = self.result_text.get("1.0", tk.END).strip()
        return len(content) == 0

    def get_results_content(self):
        """Get the current content of the results text area"""
        try:
            return self.result_text.get("1.0", tk.END).strip()
        except Exception:
            return ""

    def insert_text(self, text, position="end"):
        """Insert text at specified position"""
        self.result_text.config(state="normal")
        if position == "end":
            self.result_text.insert(tk.END, text)
        elif position == "start":
            self.result_text.insert("1.0", text)
        else:
            self.result_text.insert(position, text)
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def replace_content(self, new_content):
        """Replace all content in the results area"""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", new_content)
        self.result_text.config(state="disabled")
        self.result_text.see("1.0")

    def get_selected_text(self):
        """Get currently selected text"""
        try:
            return self.result_text.selection_get()
        except tk.TclError:
            return ""

    def scroll_to_top(self):
        """Scroll to the top of the results"""
        self.result_text.see("1.0")

    def scroll_to_bottom(self):
        """Scroll to the bottom of the results"""
        self.result_text.see(tk.END)

    def set_font(self, font_family="Consolas", font_size=11):
        """Set the font for the results text area"""
        self.result_text.config(font=(font_family, font_size))

    def set_text_colors(self, bg_color="#1e1e1e", fg_color="#ffffff", 
                       select_bg="#264f78", select_fg="white"):
        """Set colors for the text area"""
        self.result_text.config(
            bg=bg_color,
            fg=fg_color,
            selectbackground=select_bg,
            selectforeground=select_fg
        )

    def enable_editing(self):
        """Enable text editing (make text area editable)"""
        self.result_text.config(state="normal")

    def disable_editing(self):
        """Disable text editing (make text area read-only)"""
        self.result_text.config(state="disabled")

    def copy_to_clipboard(self):
        """Copy all results to clipboard"""
        try:
            content = self.get_results_content()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                return True
            return False
        except Exception:
            return False

    def find_text(self, search_text, start_pos="1.0"):
        """Find text in results and return position"""
        try:
            pos = self.result_text.search(search_text, start_pos, tk.END)
            if pos:
                # Highlight the found text
                end_pos = f"{pos}+{len(search_text)}c"
                self.result_text.tag_remove("highlight", "1.0", tk.END)
                self.result_text.tag_add("highlight", pos, end_pos)
                self.result_text.tag_config("highlight", background="yellow", foreground="black")
                self.result_text.see(pos)
                return pos
            return None
        except Exception:
            return None

    def clear_highlights(self):
        """Clear all text highlights"""
        try:
            self.result_text.tag_remove("highlight", "1.0", tk.END)
        except Exception:
            pass

    def get_line_count(self):
        """Get the number of lines in the results"""
        try:
            return int(self.result_text.index(tk.END).split('.')[0]) - 1
        except Exception:
            return 0

    def get_character_count(self):
        """Get the number of characters in the results"""
        try:
            content = self.get_results_content()
            return len(content)
        except Exception:
            return 0

    def set_wrap_mode(self, wrap_mode=tk.NONE):
        """Set text wrapping mode (tk.NONE, tk.CHAR, tk.WORD)"""
        self.result_text.config(wrap=wrap_mode)

    def show_info(self, info_message):
        """Show info message in results area with INFO prefix"""
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, f"INFO: {info_message}\n")
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def show_warning(self, warning_message):
        """Show warning message in results area with WARNING prefix"""
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, f"WARNING: {warning_message}\n")
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def append_separator(self, char="-", length=80):
        """Append a separator line to results"""
        separator = char * length + "\n"
        self.append_result(separator)

    def format_table_result(self, headers, rows, table_name=""):
        """Format and display tabular data in a readable format"""
        try:
            self.result_text.config(state="normal")
            
            if table_name:
                self.result_text.insert(tk.END, f"\n=== {table_name} ===\n")
            
            if headers and rows:
                # Calculate column widths
                col_widths = []
                for i, header in enumerate(headers):
                    max_width = len(str(header))
                    for row in rows:
                        if i < len(row):
                            max_width = max(max_width, len(str(row[i])))
                    col_widths.append(min(max_width + 2, 50))  # Cap at 50 chars
                
                # Print headers
                header_line = "|".join(str(header).ljust(col_widths[i]) for i, header in enumerate(headers))
                self.result_text.insert(tk.END, header_line + "\n")
                
                # Print separator
                separator_line = "|".join("-" * col_widths[i] for i in range(len(headers)))
                self.result_text.insert(tk.END, separator_line + "\n")
                
                # Print rows
                for row in rows:
                    row_line = "|".join(str(row[i] if i < len(row) else "").ljust(col_widths[i]) 
                                       for i in range(len(headers)))
                    self.result_text.insert(tk.END, row_line + "\n")
                
                self.result_text.insert(tk.END, f"\nRows returned: {len(rows)}\n\n")
            
            self.result_text.config(state="disabled")
            self.result_text.see(tk.END)
            
        except Exception as e:
            self.show_error(f"Error formatting table: {str(e)}")

    def show_query_timing(self, start_time, end_time, query=""):
        """Show query execution timing information"""
        try:
            execution_time = (end_time - start_time).total_seconds()
            timing_info = f"\nQuery executed in {execution_time:.3f} seconds"
            if query:
                query_preview = query[:50] + "..." if len(query) > 50 else query
                timing_info += f" - Query: {query_preview}"
            timing_info += "\n" + "="*80 + "\n"
            self.append_result(timing_info)
        except Exception as e:
            self.show_error(f"Error showing timing: {str(e)}")

    def configure_scrollbars(self):
        """Configure scrollbar behavior"""
        try:
            # Enable both horizontal and vertical scrolling
            self.result_text.config(wrap=tk.NONE)
        except Exception:
            pass

    def bind_context_menu(self):
        """Bind right-click context menu (placeholder for future implementation)"""
        def show_context_menu(event):
            # This is where you could add a context menu with Copy, Select All, etc.
            pass
        
        self.result_text.bind("<Button-3>", show_context_menu)  # Right-click

    def export_to_clipboard(self):
        """Export current results to clipboard"""
        try:
            content = self.get_results_content()
            if content:
                self.result_text.clipboard_clear()
                self.result_text.clipboard_append(content)
                return True
            return False
        except Exception:
            return False