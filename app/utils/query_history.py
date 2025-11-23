import os
import pickle
from datetime import datetime

class QueryHistoryManager:
    HISTORY_FILE = "query_history.pkl"
    MAX_HISTORY_ENTRIES = 50

    def __init__(self):
        self.query_history = []
        self.load_history()

    def add_query(self, query):
        """Add query to history"""
        self.query_history.append((datetime.now(), query))
        if len(self.query_history) > self.MAX_HISTORY_ENTRIES:
            self.query_history.pop(0)
        self.save_history()

    def load_history(self):
        """Load query history from file"""
        try:
            if os.path.exists(self.HISTORY_FILE):
                with open(self.HISTORY_FILE, 'rb') as f:
                    self.query_history = pickle.load(f)
        except Exception as e:
            print(f"Failed to load query history: {e}")
            self.query_history = []

    def save_history(self):
        """Save query history to file"""
        try:
            with open(self.HISTORY_FILE, 'wb') as f:
                pickle.dump(self.query_history, f)
        except Exception as e:
            print(f"Failed to save query history: {e}")

    def get_history(self):
        """Get query history"""
        return self.query_history

    def clear_history(self):
        """Clear all query history"""
        self.query_history = []
        self.save_history()