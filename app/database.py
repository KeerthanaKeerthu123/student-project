import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH


def get_connection(database_path: str | Path = DATABASE_PATH) -> sqlite3.Connection:
    path = str(database_path)
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(database_path: str | Path = DATABASE_PATH) -> None:
    connection = get_connection(database_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK (length(trim(name)) > 0),
                age INTEGER NOT NULL CHECK (age BETWEEN 0 AND 150),
                course TEXT NOT NULL CHECK (length(trim(course)) > 0),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()
