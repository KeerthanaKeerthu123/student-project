import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import Student, student_from_row
from app.routes.base import get_db
from app.schemas import StudentCreate, StudentRead


router = APIRouter(prefix="/students", tags=["Students"])


@router.put("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    payload: StudentCreate,
    connection: Annotated[sqlite3.Connection, Depends(get_db)],
) -> Student:
    cursor = connection.execute(
        """
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
        """,
        (payload.name, payload.age, payload.course, student_id),
    )
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    connection.commit()
    row = connection.execute(
        """
        SELECT id, name, age, course, created_at
        FROM students
        WHERE id = ?
        """,
        (student_id,),
    ).fetchone()
    return student_from_row(row)
