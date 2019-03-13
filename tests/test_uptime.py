import unittest
import urllib.request
from tests.flask_app import create_app
from ast import literal_eval
import json


class TestStats(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app = self.app.test_client()

    def tearDown(self):
        del self.app

    def __to_json(self, s):
        data = s.decode('utf8').replace("'", '"')
        data = json.loads(data)
        return data

    def test_uptime(self):
        request = self.app.get('/stats')
        data = self.__to_json(request.data)
        self.assertGreater(data["uptime"], 0)

    def test_uptime_readable(self):
        request = self.app.get('/stats')
        data = self.__to_json(request.data)
        self.assertEqual(data["uptime_readable"]["days"], 0)
        self.assertEqual(data["uptime_readable"]["hours"], 0)
        self.assertEqual(data["uptime_readable"]["minutes"], 0)
        self.assertGreater(data["uptime_readable"]["seconds"], 0)

    def test_config(self):
        request = self.app.get('/stats')
        data = self.__to_json(request.data)
        self.assertIsNotNone(data["config"])

    def test_gc_stats(self):
        request = self.app.get('/stats')
        data = self.__to_json(request.data)
        self.assertIsNotNone(data["gc_stats"])


if __name__ == '__main__':
    unittest.main()

