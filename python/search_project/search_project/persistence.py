import sqlite3

class ContextDB:
    def __init__(self, db_path='context.db'):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                conversation_history TEXT
            )
            """)

    def save_context(self, context):
        with self.connection:
            self.connection.execute("""
            INSERT INTO conversations (conversation_history) VALUES (?)
            """, (str(context.conversation.conversation_history),))

    def load_last_context(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT conversation_history FROM conversations ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            context = Context(...)  # Initialize as needed
            context.conversation.conversation_history = eval(result[0])  # Convert string back to list
            return context
        return None

    def list_last_contexts(self, limit=10):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, conversation_history FROM conversations ORDER BY id DESC LIMIT {limit}")
        return cursor.fetchall()
