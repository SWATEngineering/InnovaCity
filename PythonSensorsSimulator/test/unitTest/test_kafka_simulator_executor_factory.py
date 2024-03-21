import unittest
from unittest.mock import patch, MagicMock

from src.simulator_utils.kafka_simulator_executor_factory import KafkaSimulatorExecutorFactory
from src.simulator_utils.simulator_executor import SimulatorExecutor


class FakeAdapterProducer:
    def __init__(self, topic, ip, port):
        pass

    def produce(self, message, callback):
        pass


class TestStdoutSimulatorExecutorFactory(unittest.TestCase):
    @patch('src.writer.kafka_logic.adapter_producer.Producer')
    def test_creation(self, mock_producer):
        configs = '''
        [
  {
    "type": "humidity",
    "wait_time_in_seconds": 1.5,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "reservoir",
    "wait_time_in_seconds": 1.0,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "air_pollution",
    "wait_time_in_seconds": 1.5,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "rain",
    "wait_time_in_seconds": 1.0,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "temperature",
    "wait_time_in_seconds": 1.0,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "wind",
    "wait_time_in_seconds": 0.5,
    "location": {
      "type": "Point",
      "coordinates": [45.398256, 11.851272]
    }
  },
  {
    "type": "eco_zone",
    "wait_time_in_seconds": 5.0,
    "location": {
      "type": "Point",
      "coordinates": [
        45.398214,
        11.851271
      ]
    }
  },
  {
    "type": "parking",
    "wait_time_in_seconds": 60.0,
    "location": {
      "type": "Point",
      "coordinates": [45.409471, 11.875172]
    }
  }, 
  {
    "type": "charging_station",
    "wait_time_in_seconds": 2,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "traffic",
    "wait_time_in_seconds": 2,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  },
  {
    "type": "traffic",
    "wait_time_in_seconds": 2,
    "location": {
      "type": "Point",
      "coordinates": [45.398214, 11.851271]
    }
  }
]
        '''

        with patch('src.writer.kafka_logic.adapter_producer.AdapterProducer', FakeAdapterProducer):
            configs = configs.strip()
            factory = KafkaSimulatorExecutorFactory(configs, "", 0)
            exec_fac = factory.create()
            assert isinstance(exec_fac, SimulatorExecutor)
