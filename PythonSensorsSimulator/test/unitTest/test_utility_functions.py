import unittest
from unittest.mock import patch
from io import StringIO
from src.utils.utility_functions import acked


class TestAckedFunction(unittest.TestCase):
    def setUp(self):
        self.stdout_patch = patch('sys.stdout', new_callable=StringIO)
        self.stdout_mock = self.stdout_patch.start()

    def tearDown(self):
        self.stdout_patch.stop()

    def test_acked_success(self):
        acked(None, "Test message")
        self.assertEqual(self.stdout_mock.getvalue().strip(), '')

    def test_acked_failure(self):
        acked("Error message", "Failed message")
        expected_output = "Fallimento nella consegna del messaggio: Failed message: Error message"
        self.assertEqual(self.stdout_mock.getvalue().strip(), expected_output)
