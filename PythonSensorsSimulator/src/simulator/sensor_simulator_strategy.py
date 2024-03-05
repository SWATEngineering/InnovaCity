from datetime import timedelta, datetime
from random import Random
from abc import ABC, abstractmethod
from pydantic import BaseModel
from utils.coordinates import Coordinates


class SensorSimulatorStrategy(ABC, BaseModel):
    _wait_time_in_seconds: timedelta
    _sensor_name: str
    _random_obj: Random
    _datetime_obj: datetime
    _coordinates: Coordinates

    @abstractmethod
    def simulate(self) -> str:
        pass
