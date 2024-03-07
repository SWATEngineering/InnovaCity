import threading
from time import sleep

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.writer.writer_strategy import WriterStrategy


class SimulatorThread(threading.Thread):
    __wait_time_in_seconds: int = 1
    __is_running: bool = True
    __simulator: SensorSimulatorStrategy = None
    __writer: WriterStrategy = None

    def __init__(self, wait_time_in_seconds: int, simulator: SensorSimulatorStrategy, writer: WriterStrategy):
        super().__init__()
        self.__simulator = simulator
        self.__writer = writer
        self.__wait_time_in_seconds = wait_time_in_seconds

    def run(self) -> None:
        while self.__is_running:
            self.__writer.write(self.__simulator.simulate())
            sleep(self.__wait_time_in_seconds)

    def stop(self) -> None:
        self.__is_running = False
