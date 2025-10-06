import sqlite3

DB_FILE = 'magazine.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES authors(id) ON DELETE CASCADE,
            FOREIGN KEY(magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
