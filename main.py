from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.database import init_db
from app.routes import ai_query, create_student, delete_student, get_students, update_student


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="Student API",
    description="A SQLite-backed student API with a local Ollama question endpoint.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(create_student.router)
app.include_router(get_students.router)
app.include_router(update_student.router)
app.include_router(delete_student.router)
app.include_router(ai_query.router)


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"message": "Student API is running", "docs": "/docs"}
