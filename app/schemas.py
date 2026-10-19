from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    course: str = Field(min_length=1, max_length=100)


class StudentRead(StudentCreate):
    id: int
    created_at: str


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class QueryResponse(BaseModel):
    question: str
    answer: str
