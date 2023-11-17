from .SimulatorExecutor import SimulatorExecutor
from .Writers.Writer import Writer
from .Simulators.TemperatureSimulator import TemperatureSimulator
from .SimulatorThread import SimulatorThread


class BuilderSimulatorExecutor:
    simulator_executor: SimulatorExecutor = None
    writer: Writer = None

    def __init__(self, writer: Writer):
        self.writer = writer
        self.simulator_executor = SimulatorExecutor()

    def addTemperatureSimulator(self, id: str, frequency_in_s=1) -> "BuilderSimulatorExecutor":
        if self.writer is None:
            return self
        self.simulator_executor.simulators.append(
            SimulatorThread(
                TemperatureSimulator(self.writer, id, frequency_in_s)
            )
        )
        return self


    def getSimulatorExecutor(self) -> "SimulatorExecutor":
        symExec = self.simulator_executor
        self.simulator_executor = None
        self.writer = None
        return symExec
