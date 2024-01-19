import uuid

from abc import ABC, abstractmethod
from ..Writers import Writer


class Simulator(ABC):
    _writer: Writer = None
    _frequency_in_s: int = None
    _continue_simulating: bool = None
    _sensor_name: str = None
    _latitude: float = None
    _longitude: float = None

    def __init__(self, writer: Writer, latitude: float, longitude: float, sensor_name: str, frequency_in_s: int = 1):
        self._writer = writer
        self._frequency_in_s = frequency_in_s
        self._continue_simulating = True
        self._sensor_name = sensor_name
        self._latitude = latitude
        self._longitude = longitude

    @abstractmethod
    def simulate(self) -> None:
        pass

    def stop_simulating(self) -> None:
        self.__continue_simulating = False

    def continue_simulating(self) -> bool:
        return self.__continue_simulating
