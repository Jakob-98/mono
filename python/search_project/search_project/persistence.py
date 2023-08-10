import sqlite3
from abc import ABC, abstractmethod
from search_project.personas import Assistant
from search_project.context import Context

class ContextDB(ABC):
    @abstractmethod
    def save_context(self, context):
        pass

    @abstractmethod
    def load_last_context(self):
        pass

    @abstractmethod
    def list_last_contexts(self, limit=10):
        pass

class SL3ContextDB(ContextDB):
    def __init__(self, db_path='context.db'):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                conversation_history TEXT,
                short_description TEXT
            )
            """)

    def save_context(self, context, description=""):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO conversations (id, conversation_history, short_description) VALUES (?, ?, ?)
            """, (str(context.id), str(context.conversation.conversation_history), description))


    def load_last_context(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT conversation_history FROM conversations ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            # TODO hardcoded: Assistant
            context = Context(Assistant()) # Initialize as needed
            context.conversation.conversation_history = eval(result[0])  # Convert string back to list
            return context
        return None

    def list_last_contexts(self, limit=10):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, conversation_history FROM conversations ORDER BY id DESC LIMIT {limit}")
        return cursor.fetchall()

