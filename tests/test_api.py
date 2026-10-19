import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import get_connection, init_db
from app.routes.base import get_db
from main import app


class StudentApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "students.db"
        init_db(self.database_path)

        def get_test_db():
            connection = get_connection(self.database_path)
            try:
                yield connection
            finally:
                connection.close()

        app.dependency_overrides[get_db] = get_test_db
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.temp_dir.cleanup()

    def test_student_crud_and_validation(self) -> None:
        created = self.client.post(
            "/students",
            json={"name": " Ada Lovelace ", "age": 20, "course": "Mathematics"},
        )
        self.assertEqual(created.status_code, 201)
        student = created.json()
        self.assertEqual(student["name"], "Ada Lovelace")
        self.assertEqual(student["course"], "Mathematics")

        self.assertEqual(self.client.get("/students").json(), [student])
        self.assertEqual(
            self.client.get(f"/students/{student['id']}").json(),
            student,
        )

        updated = self.client.put(
            f"/students/{student['id']}",
            json={"name": "Ada Byron", "age": 21, "course": "Computing"},
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["name"], "Ada Byron")

        self.assertEqual(
            self.client.post(
                "/students",
                json={"name": " ", "age": -1, "course": ""},
            ).status_code,
            422,
        )
        self.assertEqual(
            self.client.delete(f"/students/{student['id']}").status_code,
            204,
        )
        self.assertEqual(self.client.get(f"/students/{student['id']}").status_code, 404)
        self.assertEqual(self.client.delete(f"/students/{student['id']}").status_code, 404)

    def test_ai_query_uses_database_records_and_returns_answer(self) -> None:
        self.client.post(
            "/students",
            json={"name": "Grace Hopper", "age": 85, "course": "Computer Science"},
        )
        model_response = type("ModelResponse", (), {"content": "One student."})()

        with patch("app.routes.ai_query.get_chat_model") as get_chat_model:
            get_chat_model.return_value.invoke.return_value = model_response
            result = self.client.post(
                "/ai/query-students",
                json={"question": "How many students study Computer Science?"},
            )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["answer"], "One student.")
        prompt = get_chat_model.return_value.invoke.call_args.args[0]
        self.assertIn("Grace Hopper", prompt)
        self.assertIn("untrusted data", prompt)


if __name__ == "__main__":
    unittest.main()
