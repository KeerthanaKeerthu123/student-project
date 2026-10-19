from collections.abc import Iterator
import sqlite3

from app.database import get_connection


def get_db() -> Iterator[sqlite3.Connection]:
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()
