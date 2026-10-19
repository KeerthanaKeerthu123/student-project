import sqlite3
from typing import TypedDict


class Student(TypedDict):
    id: int
    name: str
    age: int
    course: str
    created_at: str


def student_from_row(row: sqlite3.Row) -> Student:
    return {
        "id": row["id"],
        "name": row["name"],
        "age": row["age"],
        "course": row["course"],
        "created_at": row["created_at"],
    }
