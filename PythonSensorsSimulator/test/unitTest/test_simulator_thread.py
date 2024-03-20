import unittest
from unittest.mock import patch
from src.simulator_utils.simulator_thread import SimulatorThread
from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.writer.writer_strategy import WriterStrategy


class MockSensorSimulator(SensorSimulatorStrategy):
    def simulate(self):
        return "Mock sensor data"


class MockWriter(WriterStrategy):
    def write(self, data):
        pass


class TestSimulatorThread(unittest.TestCase):
    def test_run_method(self):
        mock_simulator = MockSensorSimulator(None,None,None,None)
        mock_writer = MockWriter()

        thread = SimulatorThread(1, mock_simulator, mock_writer)

        with patch.object(mock_simulator, 'simulate') as mock_simulate:
            with patch.object(mock_writer, 'write') as mock_write:
                thread.start()
                thread.join(timeout=2)

                # Verify that simulate method was called
                mock_simulate.assert_called()

                # Verify that write method was called
                mock_write.assert_called()

        # Clean up
        thread.stop()