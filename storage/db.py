import sqlite3
import os
from datetime import datetime


class ContentStore:
    """Handle content storage and retrieval"""

    def __init__(self, db_path="storage/content.db"):
        """Initialize the database"""

        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """Create the table"""

        schema = """
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            original_path TEXT NOT NULL,
            transformed_path TEXT NOT NULL,
            metadata TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            interaction_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content (id)
        );
        """

        conn = None
        cursor = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for query in schema.strip().split(";"):
                if query.strip():
                    cursor.execute(query)

            conn.commit()
        except Exception as e:
            raise ValueError(f"Error creating table: {str(e)}")
        finally:
            if conn:
                conn.close()

    def save_content(
        self,
        type: str,
        original_path: str,
        transformed_path: str,
        metadata: dict = None,
    ):
        """Save the content"""

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
            INSERT INTO content (type, original_path, transformed_path, metadata, created_at) 
            VALUES (?, ?, ?, ?, ?)
            """,
                (type, original_path, transformed_path, metadata, created_at),
            )

            conn.commit()

            content_id = cursor.lastrowid

            return content_id
        except Exception as e:
            raise ValueError(f"Error saving content: {str(e)}")
        finally:
            if conn:
                conn.close()
