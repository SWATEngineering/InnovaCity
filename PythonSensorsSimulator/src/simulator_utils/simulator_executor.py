from simulator_thread import SimulatorThread


class SimulatorExecutor:
    __simulators: [SimulatorThread] = []

    def __init__(self, simulators: [SimulatorThread]):
        self.__simulators = simulators

    def run_all(self) -> None:
        for simulator in self.__simulators:
            simulator.start()

    def stop_all(self) -> None:
        for simulator in self.__simulators:
            simulator.stop()

