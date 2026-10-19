import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.models import Student, student_from_row
from app.routes.base import get_db
from app.schemas import StudentCreate, StudentRead


router = APIRouter(prefix="/students", tags=["Students"])


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: StudentCreate,
    connection: Annotated[sqlite3.Connection, Depends(get_db)],
) -> Student:
    cursor = connection.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (payload.name, payload.age, payload.course),
    )
    connection.commit()
    row = connection.execute(
        "SELECT id, name, age, course, created_at FROM students WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()
    return student_from_row(row)
