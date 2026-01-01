import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestStatsEndpoints(unittest.TestCase):
    def setUp(self):
        self.test_user_id = "test_user_123"
        self.test_customer_id = "test_customer"

    def test_health_check(self):
        response = client.get("/api/v1/stats/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_get_user_stats(self):
        response = client.get(f"/api/v1/stats/user/{self.test_user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_quizzes", response.json())
        self.assertIn("average_score", response.json())

    def test_get_customer_stats(self):
        response = client.get(f"/api/v1/stats/customer/{self.test_customer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_users", response.json())
        self.assertIn("average_quizzes_per_user", response.json())

    def test_get_nonexistent_user_stats(self):
        response = client.get("/api/v1/stats/user/nonexistent-user")
        self.assertEqual(response.status_code, 404)

    def test_get_nonexistent_customer_stats(self):
        response = client.get("/api/v1/stats/customer/nonexistent-customer")
        self.assertEqual(response.status_code, 404)
        

if __name__ == '__main__':
    unittest.main() 