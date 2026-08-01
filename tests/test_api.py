import unittest
from app import create_app
from app.extensions import db

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_student(self):
        res = self.client.post("/api/students", json={
            "name": "Test",
            "email": "test@test.com"
        })
        self.assertEqual(res.status_code, 201)

    def test_get_students(self):
        res = self.client.get("/api/students")
        self.assertEqual(res.status_code, 200)

    def test_update_student(self):
        self.client.post("/api/students", json={
            "name": "Test",
            "email": "test@test.com"
        })

        res = self.client.put("/api/students/1", json={
            "name": "Updated"
        })
        self.assertEqual(res.status_code, 200)

    def test_delete_student(self):
        self.client.post("/api/students", json={
            "name": "Test",
            "email": "test@test.com"
        })

        res = self.client.delete("/api/students/1")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()