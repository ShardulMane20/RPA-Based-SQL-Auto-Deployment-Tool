import os
import hashlib
from datetime import datetime
from tkinter import filedialog, messagebox

class FileOperationsManager:
    @staticmethod
    def save_query_log(query_data, server_info):
        """Complete save query log functionality from original code"""
        if not query_data or not query_data.get('results'):
            return False, "No query results to save"
        
        try:
            # Generate filename
            query_hash = hashlib.md5(query_data['query'].encode()).hexdigest()[:8]
            timestamp = query_data['start_time'].strftime("%Y%m%d_%H%M%S")
            default_filename = f"SQLTool_{timestamp}_{query_hash}.log"
            
            # Ask user for save location
            filepath = filedialog.asksaveasfilename(
                initialfile=default_filename,
                defaultextension=".log",
                filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            
            if not filepath:
                return False, "Save cancelled by user"
            
            # Write the log file
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"SQL Tool Query Log - {timestamp}\n")
                f.write(f"Executed on server: {server_info['server']}\n")
                f.write(f"User: {server_info['username']}\n")
                f.write("-" * 80 + "\n\n")
                
                # Write query
                f.write("QUERY:\n")
                f.write(query_data['query'])
                f.write("\n\n")
                
                # Write execution info
                f.write(f"Execution time: {query_data['exec_time']:.2f} seconds\n")
                f.write(f"Total rows returned: {query_data['total_rows']}\n")
                f.write(f"Databases queried: {', '.join(query_data['databases'])}\n")
                f.write("-" * 80 + "\n\n")
                
                # Write results
                f.write("RESULTS:\n")
                for result in query_data['results']:
                    f.write(f"\nDatabase: {result['database']}\n")
                    if result['statement_num'] > 0:
                        f.write(f"Query {result['statement_num']}:\n")
                    if not result['success']:
                        f.write(f"ERROR: {result['error']}\n")
                    f.write(result['result'])
                    f.write("\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"Log generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            return True, f"Log saved successfully to:\n{filepath}"
            
        except Exception as e:
            return False, f"Failed to save log file:\n{str(e)}"

    @staticmethod
    def generate_filename(query, timestamp):
        """Generate filename for log file based on query and timestamp"""
        # Generate a hash from the query for uniqueness
        query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
        
        # Format timestamp
        if isinstance(timestamp, datetime):
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        else:
            timestamp_str = str(timestamp)
        
        # Create filename
        filename = f"SQLTool_{timestamp_str}_{query_hash}.log"
        return filename

    @staticmethod
    def save_text_file(content, default_filename=None, title="Save File"):
        """Generic method to save text content to file"""
        try:
            filepath = filedialog.asksaveasfilename(
                title=title,
                initialfile=default_filename or "output.txt",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("Log Files", "*.log"), ("All Files", "*.*")]
            )
            
            if not filepath:
                return False, "Save cancelled by user"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, f"File saved successfully to:\n{filepath}"
            
        except Exception as e:
            return False, f"Failed to save file:\n{str(e)}"

    @staticmethod
    def load_text_file(title="Open File", filetypes=None):
        """Generic method to load text content from file"""
        if filetypes is None:
            filetypes = [("Text Files", "*.txt"), ("Log Files", "*.log"), ("All Files", "*.*")]
        
        try:
            filepath = filedialog.askopenfilename(
                title=title,
                filetypes=filetypes
            )
            
            if not filepath:
                return False, "No file selected", None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return True, f"File loaded successfully from:\n{filepath}", content
            
        except Exception as e:
            return False, f"Failed to load file:\n{str(e)}", None

    @staticmethod
    def export_results_csv(results_data, default_filename=None):
        """Export query results to CSV format"""
        try:
            filepath = filedialog.asksaveasfilename(
                title="Export Results to CSV",
                initialfile=default_filename or "query_results.csv",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            
            if not filepath:
                return False, "Export cancelled by user"
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                import csv
                writer = csv.writer(f)
                
                # Write results data to CSV
                for result in results_data:
                    if isinstance(result, dict) and 'rows' in result:
                        # Write headers if available
                        if result.get('headers'):
                            writer.writerow(result['headers'])
                        
                        # Write data rows
                        for row in result['rows']:
                            writer.writerow(row)
                        
                        # Add separator between result sets
                        writer.writerow([])
            
            return True, f"Results exported successfully to:\n{filepath}"
            
        except Exception as e:
            return False, f"Failed to export results:\n{str(e)}"

    @staticmethod
    def create_backup_filename(original_filename):
        """Create a backup filename with timestamp"""
        name, ext = os.path.splitext(original_filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{name}_backup_{timestamp}{ext}"

    @staticmethod
    def ensure_directory_exists(filepath):
        """Ensure the directory for the given filepath exists"""
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return True

    @staticmethod
    def get_safe_filename(filename):
        """Remove/replace unsafe characters from filename"""
        import re
        # Remove or replace unsafe characters
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        if len(safe_filename) > 200:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = name[:200-len(ext)] + ext
        return safe_filename

    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
