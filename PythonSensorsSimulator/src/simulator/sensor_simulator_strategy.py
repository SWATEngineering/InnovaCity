from datetime import timedelta, datetime
from random import Random
from abc import ABC, abstractmethod
from pydantic import BaseModel
from src.utils.coordinates import Coordinates


class SensorSimulatorStrategy(ABC, BaseModel):
    _sensor_name: str
    _random_obj: Random
    _datetime_obj: datetime
    _coordinates: Coordinates

    def __init__(self, **data):
        super().__init__(**data)
        self._sensor_name = data['sensor_name']
        self._random_obj = data['random_obj']
        self._datetime_obj = data['datetime_obj']
        self._coordinates = data['coordinates']

    @abstractmethod
    def simulate(self) -> str:
        pass
