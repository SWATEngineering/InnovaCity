import unittest
from io import StringIO
from unittest.mock import patch
from src.writer.std_out_writer import StdoutWriter


class TestStdoutWriter(unittest.TestCase):
    def setUp(self):
        self.stdout_patch = patch('sys.stdout', new_callable=StringIO)
        self.stdout_mock = self.stdout_patch.start()
        self.writer = StdoutWriter()

    def tearDown(self):
        self.stdout_patch.stop()

    def test_write(self):
        self.writer.write("Test message")
        self.assertEqual(self.stdout_mock.getvalue().strip(), "Test message")


if __name__ == '__main__':
    unittest.main()
