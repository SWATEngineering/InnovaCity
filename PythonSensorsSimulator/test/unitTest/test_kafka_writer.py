import unittest
from unittest.mock import MagicMock
from src.writer.kafka_writer import KafkaWriter
from src.writer.kafka_logic.target_producer import TargetProducer
from src.utils.utility_functions import acked


class TestKafkaWriter(unittest.TestCase):
    def test_write(self):
        # Mocking TargetProducer
        mock_producer = MagicMock(spec=TargetProducer)
        writer = KafkaWriter(mock_producer)

        # Action
        writer.write("Test message")

        # Assertion
        mock_producer.produce.assert_called_once_with("Test message", acked)
