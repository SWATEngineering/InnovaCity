import unittest
from unittest.mock import MagicMock
from src.writer.kafka_logic.adapter_producer import AdapterProducer
from src.utils.sensor_types import SensorTypes


class TestAdapterProducer(unittest.TestCase):
    def test_produce_success(self):
        # Setup
        mock_producer = MagicMock()
        adapter = AdapterProducer(SensorTypes.TEMPERATURE, 'localhost', 9092)
        adapter._AdapterProducer__producer = mock_producer

        # Action
        adapter.produce('Test Message', None)

        # Assertion
        mock_producer.produce.assert_called_once_with(
            SensorTypes.TEMPERATURE.value,
            value='Test Message',
            callback=None
        )

    def test_produce_failure(self):
        # Setup
        mock_producer = MagicMock()
        mock_producer.produce.side_effect = Exception('Producer error')
        adapter = AdapterProducer(SensorTypes.HUMIDITY, 'localhost', 9092)
        adapter._AdapterProducer__producer = mock_producer

        # Action & Assertion
        with self.assertRaises(Exception):
            adapter.produce('Test Message', None)


if __name__ == '__main__':
    unittest.main()
