# Student API

A FastAPI CRUD service backed by SQLite, with an optional natural-language
student-record query endpoint powered by a local Ollama model.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull llama3.2:1b
uvicorn main:app --reload
```

The API creates `students.db` on first startup. Open
<http://127.0.0.1:8000/docs> for interactive API documentation.

Set `STUDENTS_DB_PATH` to change the SQLite file, `OLLAMA_MODEL` to select a
different Ollama model, or `OLLAMA_BASE_URL` if Ollama is running elsewhere.
The CRUD endpoints work without Ollama; the AI endpoint requires the
`langchain-ollama` package and a running Ollama server.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/students` | Create a student (`name`, `age`, `course`) |
| `GET` | `/students` | List students (`limit` and `offset` supported) |
| `GET` | `/students/{student_id}` | Get one student |
| `PUT` | `/students/{student_id}` | Replace a student's name, age, and course |
| `DELETE` | `/students/{student_id}` | Delete a student |
| `POST` | `/ai/query-students` | Ask a question about student records |

Example request for the AI endpoint:

```json
{
  "question": "How many students are enrolled in Computer Science?"
}
```
