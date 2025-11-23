class QueryValidator:
    @staticmethod
    def contains_dangerous_sql(query: str) -> bool:
        """Detect destructive SQL operations."""
        lowered = query.lower()
        destructive_keywords = [
            "drop table", "drop database", "truncate table",
            "delete from", "alter table", "update "
        ]
        return any(keyword in lowered for keyword in destructive_keywords)

    @staticmethod
    def validate_query(query: str) -> tuple[bool, str]:
        """Validate SQL query"""
        if not query.strip():
            return False, "Query cannot be empty"
        
        if QueryValidator.contains_dangerous_sql(query):
            return False, "Query contains potentially destructive operations"
        
        return True, "Query is valid"
