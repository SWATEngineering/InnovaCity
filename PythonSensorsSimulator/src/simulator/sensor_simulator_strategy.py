from datetime import datetime
from random import Random
from abc import ABC, abstractmethod
from typing import Type

from src.utils.coordinates import Coordinates


class SensorSimulatorStrategy(ABC):
    _sensor_name: str
    _random_obj: Random
    _datetime_obj: Type[datetime]
    _coordinates: Coordinates

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        self._sensor_name = sensor_name
        self._random_obj = random_obj
        self._datetime_obj = datetime_obj
        self._coordinates = coordinates

    @abstractmethod
    def simulate(self) -> str:
        pass
