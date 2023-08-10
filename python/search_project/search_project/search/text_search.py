import sqlite3

class TextDatabase:
    def __init__(self, db_path='./persistence/text_data.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS text_data USING fts5(content);
            """)

    def insert_text(self, text):
        with self.conn:
            self.conn.execute("""
            INSERT INTO text_data(content) VALUES (?);
            """, (text,))

    def search_text(self, query, max_chars=64, k=10):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT snippet(text_data, 0, '<b>', '</b>', '...', {max_chars}) FROM text_data WHERE content MATCH ? LIMIT {k};
        """, (query,))
        return cursor.fetchall()


db = TextDatabase()
