import sqlite3
from datetime import datetime

DB_NAME = "urls.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_short_code ON urls (short_code)")
    conn.commit()
    conn.close()

def create_short_url(short_code: str, original_url: str) -> bool:
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO urls (short_code, original_url, created_at) VALUES (?, ?, ?)",
            (short_code, original_url, datetime.utcnow().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_url_and_increment(short_code: str):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,)).fetchone()
    if row:
        conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
        conn.commit()
    conn.close()
    return dict(row) if row else None

def get_url_stats(short_code: str):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,)).fetchone()
    conn.close()
    return dict(row) if row else None
