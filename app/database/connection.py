import pyodbc
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self):
        self.current_server = None
        self.conn = None

    @contextmanager
    def database_connection(self, database="master"):
        """Context manager for database connections"""
        if not self.current_server:
            raise ValueError("No server configuration available")
            
        conn = None
        try:
            conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={self.current_server["server"]};'
                f'DATABASE={database};UID={self.current_server["username"]};'
                f'PWD={self.current_server["password"]}',
                timeout=10
            )
            yield conn
        finally:
            if conn:
                conn.close()

    def set_server_config(self, server, username, password):
        self.current_server = {
            'server': server,
            'username': username,
            'password': password
        }

    def test_connection(self):
        """Test database connection"""
        try:
            with self.database_connection("master") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                return True, "Connected successfully"
        except Exception as e:
            return False, str(e)

    def get_databases(self):
        """Get list of available databases"""
        try:
            with self.database_connection("master") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4 AND state = 0 ORDER BY name")
                return [db[0] for db in cursor.fetchall()]
        except Exception as e:
            raise Exception(f"Failed to fetch databases: {e}")
