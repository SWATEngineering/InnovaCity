import threading
from .Simulators.Simulator import Simulator


class SimulatorThread(threading.Thread):
    simulator: Simulator = None

    def __init__(self, simulator: Simulator):
        super().__init__()
        self.simulator = simulator

    def run(self) -> None:
        self.simulator.simulate()

    def stop(self) -> None:
        self.simulator.stop_simulating()
