from simulator_thread import SimulatorThread
from pydantic import BaseModel


class SimulatorExecutor(BaseModel):
    __simulators: [SimulatorThread] = []

    def run_all(self) -> None:
        for simulator in self.__simulators:
            simulator.start()

    def stop_all(self) -> None:
        for simulator in self.__simulators:
            simulator.stop()

