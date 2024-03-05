import threading

from simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from writer.writer_strategy import WriterStrategy


class SimulatorThread(threading.Thread):
    __is_running = True
    __simulator: SensorSimulatorStrategy = None
    __writer: WriterStrategy = None

    def __init__(self, simulator: SensorSimulatorStrategy, writer: WriterStrategy):
        super().__init__()
        self.__simulator = simulator
        self.__writer = writer

    def run(self) -> None:
        while self.__is_running:
            self.__writer.write(self.__simulator.simulate())

    def stop(self) -> None:
        self.__is_running = False
