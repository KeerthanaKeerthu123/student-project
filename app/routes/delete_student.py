import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.routes.base import get_db


router = APIRouter(prefix="/students", tags=["Students"])


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: int,
    connection: Annotated[sqlite3.Connection, Depends(get_db)],
) -> Response:
    cursor = connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
