import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models import Student, student_from_row
from app.routes.base import get_db
from app.schemas import StudentRead


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=list[StudentRead])
def list_students(
    connection: Annotated[sqlite3.Connection, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Student]:
    rows = connection.execute(
        """
        SELECT id, name, age, course, created_at
        FROM students
        ORDER BY id
        LIMIT ? OFFSET ?
        """,
        (limit, offset),
    ).fetchall()
    return [student_from_row(row) for row in rows]


@router.get("/{student_id}", response_model=StudentRead)
def get_student(
    student_id: int,
    connection: Annotated[sqlite3.Connection, Depends(get_db)],
) -> Student:
    row = connection.execute(
        """
        SELECT id, name, age, course, created_at
        FROM students
        WHERE id = ?
        """,
        (student_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student_from_row(row)
