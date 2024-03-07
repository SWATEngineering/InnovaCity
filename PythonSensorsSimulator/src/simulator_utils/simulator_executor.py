from src.simulator_utils.simulator_thread import SimulatorThread

from pydantic import BaseModel


class SimulatorExecutor(BaseModel):
    __simulators: [SimulatorThread] = []

    def __init__(self,**data):
        super().__init__(**data)
        self.__simulators = data['simulators']

    def run_all(self) -> None:
        for simulator in self.__simulators:
            simulator.start()

    def stop_all(self) -> None:
        for simulator in self.__simulators:
            simulator.stop()

