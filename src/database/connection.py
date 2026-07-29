import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

DATABASE_URL = os.environ.get("DATABASE_URL")

@contextmanager
def get_db_connection():
    """Context manager to get a database connection."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """Context manager to get a database cursor with dict support."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                yield cur
                if commit:
                    conn.commit()
            except Exception:
                conn.rollback()
                raise
