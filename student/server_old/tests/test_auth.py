import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient
from main import app
from models.auth import UserAuth0Request

client = TestClient(app)

class TestAuthEndpoints(unittest.TestCase):
    def setUp(self):
        self.test_user = UserAuth0Request(
            email='test@test.com',
            full_name='Test User',
            sub='auth0|123456789'
        )

    def test_health_check(self):
        response = client.get("/api/v1/auth/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_create_user_success(self):
        response = client.post(
            "/api/v1/auth/create",
            json=self.test_user.dict()
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json())

    def test_create_user_invalid_email(self):
        invalid_user = self.test_user.copy()
        invalid_user.email = "invalid-email"
        response = client.post(
            "/api/v1/auth/create",
            json=invalid_user.dict()
        )
        self.assertEqual(response.status_code, 422)

    def test_get_user_by_id(self):
        # First create a user
        create_response = client.post(
            "/api/v1/auth/create",
            json=self.test_user.dict()
        )
        user_id = create_response.json()["user_id"]

        # Then try to get the user
        response = client.get(f"/api/v1/auth/user/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], self.test_user.email)

    def test_get_nonexistent_user(self):
        response = client.get("/api/v1/auth/user/nonexistent-id")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 