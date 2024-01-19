from .SimulatorExecutor import SimulatorExecutor
from .Writers.Writer import Writer
from .Simulators.TemperatureSimulator import TemperatureSimulator
from .Simulators.RainSimulator import RainSimulator
from .SimulatorThread import SimulatorThread


class SimulatorExecutorAggregator:
    __simulator_executor: SimulatorExecutor = None

    def __init__(self):
        self.__simulator_executor = SimulatorExecutor()

    def add_temperature_simulator(
            self,
            writer: Writer,
            latitude: float,
            longitude: float,
            frequency_in_s=1
    ) -> "SimulatorExecutorAggregator":
        if writer is None:
            return self

        self.__simulator_executor.append_simulator(
            SimulatorThread(
                TemperatureSimulator(
                    writer, latitude, longitude, frequency_in_s)
            )
        )
        return self

    def add_rain_simulator(
        self,
        writer: Writer,
        latitude: float,
        longitude: float,
        frequency_in_s=1
    ) -> "SimulatorExecutorAggregator":
        if writer is None:
            return self

        self.__simulator_executor.append_simulator(
            SimulatorThread(
                RainSimulator(
                    writer, latitude, longitude, frequency_in_s)
            )
        )
        return self

    def get_simulator_executor(self) -> "SimulatorExecutor":
        sym_exec = self.__simulator_executor
        self.__simulator_executor = SimulatorExecutor()
        return sym_exec
