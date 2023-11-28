from .SimulatorExecutor import SimulatorExecutor
from .Writers.Writer import Writer
from .Simulators.TemperatureSimulator import TemperatureSimulator
from .SimulatorThread import SimulatorThread


class BuilderSimulatorExecutor:
    __simulator_executor: SimulatorExecutor = None

    def __init__(self):
        self.__simulator_executor = SimulatorExecutor()

    def add_temperature_simulator(self, writer: Writer, id: str, frequency_in_s=1) -> "BuilderSimulatorExecutor":
        if writer is None:
            return self
        self.__simulator_executor._SimulatorExecutor__simulators.append(
            SimulatorThread(
                TemperatureSimulator(writer, id, frequency_in_s)
            )
        )
        return self

    def get_simulator_executor(self) -> "SimulatorExecutor":
        sym_exec = self.__simulator_executor
        self.__simulator_executor = SimulatorExecutor()
        return sym_exec
