from PythonSensorsSimulator.Model import SimulatorThread


class SimulatorExecutor:
    simulators: [SimulatorThread] = []

    def __init__(self):
        pass

    def run_all(self) -> None:
        for simulator in self.simulators:
            simulator.start()

    def stop_all(self) -> None:
        for simulator in self.simulators:
            simulator.stop()
