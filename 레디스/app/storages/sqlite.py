import os
import sqlite3
from pathlib import Path


def _sqlite_path() -> Path:
    return Path(os.getenv("SQLITE_PATH", "data/redis-study.sqlite3"))


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection for the source-of-truth store.

    Returns:
        SQLite connection with row access by column name.
    """
    db_path = _sqlite_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the minimal table used by the cache-aside examples.

    Returns:
        None.
    """
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
            """
        )
