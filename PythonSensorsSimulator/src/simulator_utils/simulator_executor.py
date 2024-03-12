from typing import List

from src.simulator_utils.simulator_thread import SimulatorThread


class SimulatorExecutor:
    __simulators: List[SimulatorThread] = []

    def __init__(self, simulators: List[SimulatorThread]):
        self.__simulators = simulators

    def run_all(self) -> None:
        for simulator in self.__simulators:
            simulator.start()

    def stop_all(self) -> None:
        for simulator in self.__simulators:
            simulator.stop()
