import time
import pyodbc
import re
from datetime import datetime

class QueryExecutor:
        def __init__(self, db_manager, message_queue):
            self.db_manager = db_manager
            self.message_queue = message_queue

        def execute_query(self, databases, query):
            """Execute query against multiple databases"""
            # Fix: Ensure query is a string, not a list
            if isinstance(query, list):
                query = ' '.join(query)
            elif not isinstance(query, str):
                query = str(query)
            
            # Validate inputs
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            
            if not databases:
                raise ValueError("No databases selected")
            
            start_time = time.time()
            overall_total_rows = 0
            databases_info = []
            
            # Split the query into individual statements - FIXED for stored procedures
            statements = self._split_sql_statements(query)
            
            if not statements:
                raise ValueError("No valid SQL statements found")
            
            for db in databases:
                db_info = self._execute_on_database(db, statements)
                databases_info.append(db_info)
                overall_total_rows += db_info['total_rows']
            
            total_exec_time = time.time() - start_time
            
            # Generate and send results
            self._send_results(databases_info, total_exec_time, overall_total_rows)
            
            return {
                'exec_time': total_exec_time,
                'total_rows': overall_total_rows,
                'databases_info': databases_info
            }

        def _split_sql_statements(self, query):
            """Split SQL query into individual statements - ENHANCED VERSION FOR PROCEDURE OPERATIONS"""
            # Clean up the query
            query = query.strip()
            if not query:
                return []
            
            # First, check for GO statements (SQL Server batch separators)
            # GO statements should split the query into separate batches
            if re.search(r'^\s*GO\s*$', query, re.MULTILINE | re.IGNORECASE):
                # Split by GO statements first
                batches = re.split(r'^\s*GO\s*$', query, flags=re.MULTILINE | re.IGNORECASE)
                
                statements = []
                for batch in batches:
                    batch = batch.strip()
                    if batch:
                        # Each batch is treated as a single statement
                        statements.append(batch)
                
                return [stmt for stmt in statements if stmt and stmt.strip()]
            
            # Check for DROP + CREATE procedure pattern (without GO)
            # This handles the specific case of DROP PROCEDURE followed by CREATE PROCEDURE
            # More robust pattern matching
            
            # Look for IF OBJECT_ID...DROP PROCEDURE pattern
            if_drop_match = re.search(
                r'(IF\s+OBJECT_ID\s*\([^)]+\)\s+IS\s+NOT\s+NULL\s+DROP\s+PROCEDURE\s+[^;]+;)',
                query,
                re.DOTALL | re.IGNORECASE
            )
            
            # Look for CREATE PROCEDURE pattern  
            create_match = re.search(
                r'(CREATE\s+PROCEDURE\s+.*)',
                query,
                re.DOTALL | re.IGNORECASE
            )
            
            # If we found both patterns, split them
            if if_drop_match and create_match:
                drop_part = if_drop_match.group(1).strip()
                
                # Get everything after the DROP statement as the CREATE part
                drop_end = if_drop_match.end()
                create_part = query[drop_end:].strip()
                
                # Clean up the CREATE part (remove leading comments/whitespace)
                create_lines = create_part.split('\n')
                cleaned_create_lines = []
                found_create = False
                
                for line in create_lines:
                    line_stripped = line.strip()
                    if line_stripped.startswith('--'):
                        if found_create:
                            break  # Stop at first comment after CREATE
                        continue  # Skip comments before CREATE
                    if line_stripped.upper().startswith('CREATE'):
                        found_create = True
                    if found_create or line_stripped:
                        cleaned_create_lines.append(line)
                
                if cleaned_create_lines:
                    create_part = '\n'.join(cleaned_create_lines).strip()
                    return [drop_part, create_part]
            
            # Remove single-line comments but preserve the structure
            lines = query.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove comments but keep the line structure
                if '--' in line:
                    comment_pos = line.find('--')
                    line = line[:comment_pos].rstrip()
                cleaned_lines.append(line)
            query = '\n'.join(cleaned_lines)
            
            # Remove multi-line comments
            query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
            query = query.strip()
            
            # Check for complex statements that should NOT be split
            complex_patterns = [
                # CREATE/ALTER/DROP procedures
                r'\b(CREATE|ALTER|DROP)\s+(PROCEDURE|PROC)\s+',
                # CREATE/ALTER/DROP functions  
                r'\b(CREATE|ALTER|DROP)\s+(FUNCTION|FUNC)\s+',
                # CREATE/ALTER/DROP triggers
                r'\b(CREATE|ALTER|DROP)\s+TRIGGER\s+',
                # CREATE/ALTER/DROP views with complex definitions
                r'\b(CREATE|ALTER|DROP)\s+VIEW\s+.*?\bAS\b.*?\bSELECT\b',
                # Stored procedure execution
                r'\b(EXEC|EXECUTE)\s+\w+',
                # DECLARE blocks (variable declarations)
                r'\bDECLARE\s+@\w+',
                # Complex BEGIN...END blocks
                r'\bBEGIN\b.*?\bEND\b'
            ]
            
            # Check if this is a complex statement that shouldn't be split
            for pattern in complex_patterns:
                if re.search(pattern, query, re.IGNORECASE | re.DOTALL):
                    # For CREATE PROCEDURE and similar complex statements, return as single statement
                    if re.search(r'\b(CREATE|ALTER|DROP)\s+(PROCEDURE|PROC|FUNCTION|FUNC|TRIGGER)\s+', query, re.IGNORECASE):
                        return [query]
                    # For EXEC statements, also return as single statement
                    elif re.search(r'\b(EXEC|EXECUTE)\s+\w+', query, re.IGNORECASE):
                        return [query]
            
            # For regular SQL, use intelligent splitting
            statements = []
            current_statement = ""
            in_string = False
            string_char = None
            in_bracket = False
            bracket_depth = 0
            paren_depth = 0
            begin_end_depth = 0
            
            i = 0
            while i < len(query):
                char = query[i]
                
                # Handle string literals
                if char in ("'", '"') and not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char and in_string:
                    # Check for escaped quotes
                    if i + 1 < len(query) and query[i + 1] == string_char:
                        current_statement += char + char
                        i += 1
                    else:
                        in_string = False
                        string_char = None
                
                # Handle square brackets (for identifiers)
                elif char == '[' and not in_string:
                    in_bracket = True
                elif char == ']' and in_bracket and not in_string:
                    in_bracket = False
                
                # Track depths outside of strings and brackets
                elif not in_string and not in_bracket:
                    if char == '(':
                        paren_depth += 1
                    elif char == ')':
                        paren_depth -= 1
                    elif query[i:i+5].upper() == 'BEGIN':
                        # Make sure it's a word boundary
                        if (i == 0 or not query[i-1].isalnum()) and (i+5 >= len(query) or not query[i+5].isalnum()):
                            begin_end_depth += 1
                    elif query[i:i+3].upper() == 'END':
                        # Make sure it's a word boundary  
                        if (i == 0 or not query[i-1].isalnum()) and (i+3 >= len(query) or not query[i+3].isalnum()):
                            begin_end_depth = max(0, begin_end_depth - 1)
                    elif char == ';' and paren_depth == 0 and begin_end_depth == 0:
                        # This is a true statement separator
                        if current_statement.strip():
                            statements.append(current_statement.strip())
                        current_statement = ""
                        i += 1
                        continue
                
                current_statement += char
                i += 1
            
            # Add the last statement
            if current_statement.strip():
                statements.append(current_statement.strip())
            
            # If we only got one statement and it contains CREATE PROCEDURE, return it as-is
            if len(statements) == 1 and re.search(r'\b(CREATE|ALTER)\s+(PROCEDURE|PROC)\s+', statements[0], re.IGNORECASE):
                return statements
            
            # Filter out empty statements
            return [stmt for stmt in statements if stmt and stmt.strip()]

        def _execute_on_database(self, db, statements):
            """Execute statements on a single database"""
            db_start_time = time.time()
            db_total_rows = 0
            db_errors = []
            db_statement_count = 0
            db_results = []
            
            try:
                self.message_queue.put(("status", f"🔄 Connecting to {db}..."))
                
                with self.db_manager.database_connection(db) as conn:
                    cursor = conn.cursor()
                    total_statements = len(statements)
                    
                    for i, statement in enumerate(statements, 1):
                        db_statement_count += 1
                        try:
                            # For each statement, execute it completely
                            cursor.execute(statement)
                            
                            # Handle multiple result sets (especially for stored procedures)
                            result_sets = []
                            
                            while True:
                                rows = []
                                if cursor.description:
                                    # Fetch rows in batches to avoid memory issues
                                    while True:
                                        batch = cursor.fetchmany(1000)
                                        if not batch:
                                            break
                                        rows.extend(batch)
                                    
                                    if rows:
                                        result_sets.append((cursor.description, rows))
                                else:
                                    # No result set, but might have affected rows
                                    result_sets.append((None, cursor.rowcount))
                                
                                # Move to next result set
                                if not cursor.nextset():
                                    break
                            
                            # Format results
                            if result_sets:
                                for j, result_set in enumerate(result_sets):
                                    description, data = result_set
                                    if description:  # Has columns
                                        result = self._format_query_results(description, data, db, i, j+1 if len(result_sets) > 1 else None)
                                        db_results.append(result)
                                        db_total_rows += len(data)
                                    else:  # Just row count
                                        if data > 0:
                                            result = f"\n{'═' * 80}\n📋 Statement {i} executed on {db}\n{'═' * 80}\n✅ Rows affected: {data}\n{'═' * 80}\n"
                                        else:
                                            result = f"\n{'═' * 80}\n📋 Statement {i} executed on {db}\n{'═' * 80}\n✅ Command completed successfully\n{'═' * 80}\n"
                                        db_results.append(result)
                            else:
                                # No results at all
                                result = f"\n{'═' * 80}\n📋 Statement {i} executed on {db}\n{'═' * 80}\n✅ Command completed successfully\n{'═' * 80}\n"
                                db_results.append(result)
                            
                            # Commit after each statement to ensure it's completed
                            conn.commit()
                            
                        except pyodbc.DatabaseError as e:
                            error_msg = f"\n{'═' * 80}\nError in Statement {i} on {db}: {str(e)}\n{'═' * 80}\n"
                            db_results.append(error_msg)
                            db_errors.append(f"Statement {i}: {str(e)}")
                            # Don't break - continue with next statement
                    
            except Exception as e:
                error_msg = f"\n{'═' * 80}\nConnection error with {db}: {str(e)}\n{'═' * 80}\n"
                db_results.append(error_msg)
                db_errors.append(f"Connection: {str(e)}")
            
            db_exec_time = time.time() - db_start_time
            
            return {
                'name': db,
                'exec_time': db_exec_time,
                'total_rows': db_total_rows,
                'status': 'Success' if not db_errors else 'Error',
                'statement_count': db_statement_count,
                'errors': db_errors,
                'results': db_results
            }

        def _format_query_results(self, description, rows, db_name, statement_num, result_set_num=None):
            """Format query results for display with enhanced tabular styling"""
            # Build title
            title = f"📋 Results from Statement {statement_num} on {db_name}"
            if result_set_num:
                title += f" (Result Set {result_set_num})"
            
            if not rows:
                return f"\n{'═' * 80}\n{title}\n{'═' * 80}\n⚠️  No rows returned\n{'═' * 80}\n"
            
            column_names = [c[0] for c in description]
            
            # Calculate column widths with minimum and maximum limits
            min_width = 8
            max_width = 30
            col_widths = []
            
            for i, name in enumerate(column_names):
                # Calculate width based on column name and data
                name_width = len(str(name))
                data_widths = [len(str(row[i])) for row in rows[:100]]  # Sample first 100 rows for performance
                max_data_width = max(data_widths) if data_widths else 0
                
                # Set width with constraints
                width = max(min_width, min(max_width, max(name_width, max_data_width)))
                col_widths.append(width)
            
            # Build the table with box drawing characters
            def truncate_text(text, width):
                text = str(text)
                if len(text) <= width:
                    return text
                return text[:width-3] + "..."
            
            # Header section
            header_line = f"\n{'═' * 100}\n"
            title_line = f"{title} (Showing {len(rows):,} rows)\n"
            separator_line = f"{'═' * 100}\n"
            
            # Column headers with box drawing
            header_top = "┌" + "┬".join("─" * (width + 2) for width in col_widths) + "┐"
            header_content = "│ " + " │ ".join(
                str(name).ljust(width) for name, width in zip(column_names, col_widths)
            ) + " │"
            header_bottom = "├" + "┼".join("─" * (width + 2) for width in col_widths) + "┤"
            
            # Data rows
            data_rows = []
            for row in rows:
                row_content = "│ " + " │ ".join(
                    truncate_text(value, width).ljust(width)
                    for value, width in zip(row, col_widths)
                ) + " │"
                data_rows.append(row_content)
            
            # Table footer
            table_footer = "└" + "┴".join("─" * (width + 2) for width in col_widths) + "┘"
            
            # Combine all parts
            table_parts = [
                header_line,
                title_line,
                separator_line,
                header_top,
                header_content,
                header_bottom,
                *data_rows,
                table_footer,
                f"\n✅ Total rows: {len(rows):,}\n{'═' * 100}\n"
            ]
            
            return "\n".join(table_parts)

        def _send_results(self, databases_info, total_exec_time, overall_total_rows):
            """Send results to message queue"""
            # Generate and send the detailed execution summary first
            summary = self._generate_execution_summary(databases_info, total_exec_time, overall_total_rows)
            self.message_queue.put(("execution_summary", summary))
            
            # Send results in reverse order (last executed database first)
            for db_info in reversed(databases_info):
                for result in db_info['results']:
                    self.message_queue.put(("result", result))

        def _generate_execution_summary(self, databases_info, total_exec_time, overall_total_rows):
            """Generate execution summary in clean tabular format"""
            from datetime import datetime
            
            # Summary header
            summary_lines = []
            summary_lines.append("=" * 100)
            summary_lines.append("EXECUTION SUMMARY")
            summary_lines.append("=" * 100)
            summary_lines.append(f"Total Execution Time: {total_exec_time:.3f} seconds")
            summary_lines.append(f"Overall Total Rows  : {overall_total_rows:,}")
            summary_lines.append(f"Databases Processed : {len(databases_info)}")
            summary_lines.append(f"Executed At         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            summary_lines.append("")
            
            # Database results table
            summary_lines.append("DATABASE EXECUTION DETAILS")
            summary_lines.append("=" * 100)
            
            # Table headers
            headers = ["Database", "Time(s)", "Rows", "Statements", "Status", "Errors"]
            col_widths = [20, 10, 12, 12, 10, 30]
            
            # Header row
            header_row = "|"
            for header, width in zip(headers, col_widths):
                header_row += f" {header:<{width-1}}|"
            summary_lines.append(header_row)
            
            # Separator row
            sep_row = "|"
            for width in col_widths:
                sep_row += "-" * width + "|"
            summary_lines.append(sep_row)
            
            # Data rows
            for db_info in reversed(databases_info):
                db_name = db_info['name'][:19]  # Truncate if too long
                db_time = f"{db_info['exec_time']:.3f}"
                db_rows = f"{db_info['total_rows']:,}"
                db_statements = str(db_info['statement_count'])
                db_status = db_info['status']
                
                # Format errors
                if db_info.get('errors'):
                    error_summary = f"{len(db_info['errors'])} error(s)"
                    if len(db_info['errors']) == 1:
                        error_detail = db_info['errors'][0][:25] + "..." if len(db_info['errors'][0]) > 25 else db_info['errors'][0]
                        error_summary = error_detail
                else:
                    error_summary = "None"
                
                # Build row
                row_data = [db_name, db_time, db_rows, db_statements, db_status, error_summary]
                data_row = "|"
                for data, width in zip(row_data, col_widths):
                    data_row += f" {str(data):<{width-1}}|"
                summary_lines.append(data_row)
            
            # Table footer
            summary_lines.append(sep_row)
            summary_lines.append("=" * 100)
            summary_lines.append("")
            
            return "\n".join(summary_lines)