import unittest
from unittest.mock import MagicMock
from src.simulator_utils.simulator_thread import SimulatorThread
from src.simulator_utils.simulator_executor import SimulatorExecutor


class TestSimulatorExecutor(unittest.TestCase):
    def setUp(self):
        self.simulator1 = MagicMock(spec=SimulatorThread)
        self.simulator2 = MagicMock(spec=SimulatorThread)
        self.simulator3 = MagicMock(spec=SimulatorThread)
        self.simulators = [self.simulator1, self.simulator2, self.simulator3]
        self.executor = SimulatorExecutor(self.simulators)

    def test_run_all(self):
        self.executor.run_all()
        for simulator in self.simulators:
            simulator.start.assert_called_once()

    def test_stop_all(self):
        self.executor.stop_all()
        for simulator in self.simulators:
            simulator.stop.assert_called_once()