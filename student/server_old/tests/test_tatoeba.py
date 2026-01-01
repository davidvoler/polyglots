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

        

if __name__ == '__main__':
    unittest.main() 