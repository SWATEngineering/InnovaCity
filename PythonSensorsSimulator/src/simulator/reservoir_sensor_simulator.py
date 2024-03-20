from datetime import datetime
from random import Random
from typing import Type

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
import math
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
from src.utils.coordinates import Coordinates


class ReservoirSensorSimulator(SensorSimulatorStrategy):
    __reservoir_percentage: float

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self._set_reservoir_percentage()
        
    def _set_reservoir_percentage(self) -> None:
        month = self._datetime_obj.now().month
        if 3 <= month < 6:
            self.__reservoir_percentage = self._random_obj.uniform(80, 85)
        elif 6 <= month < 9:
            self.__reservoir_percentage = self._random_obj.uniform(75, 80)
        elif 9 <= month < 12:
            self.__reservoir_percentage = self._random_obj.uniform(85, 90)
        else:
            self.__reservoir_percentage = self._random_obj.uniform(90, 95)
        
    def _calculate_evaporation_rate(self) -> float:

        hour = self._datetime_obj.now().hour
        month = self._datetime_obj.now().month
        base_evaporation_rate = ((math.cos(math.pi * ((hour - 12) / 12)) + 1) / 2) * 0.4 + 0.3

        if 3 <= month < 6:
            base_evaporation_rate += 0.2
        elif 6 <= month < 9:
            base_evaporation_rate += 0.4
        elif 9 <= month < 12:
            base_evaporation_rate -= 0.1
        else:
            base_evaporation_rate -= 0.2

        evaporation_rate = base_evaporation_rate + self._random_obj.uniform(-0.05, 0.05)
        evaporation_rate = max(0, min(1, evaporation_rate))

        return evaporation_rate

    def _measure_reservoir_level(self) -> float:
        current_time = self._datetime_obj.now()
        hour = current_time.hour
        month = current_time.month

        evaporation_rate = self._calculate_evaporation_rate()
        evaporation_change = self._random_obj.uniform(-0.1, 0.1) * evaporation_rate
        total_change = self._random_obj.uniform(-0.1, 0.1) + evaporation_change

        percentage = max(0, min(100, self.__reservoir_percentage + total_change))

        return percentage

    def simulate(self) -> str:
        timestamp = self._datetime_obj.now()
        self.__reservoir_percentage = self._measure_reservoir_level()

        reading = {
            "type": "%",
            "value": round(self.__reservoir_percentage, 2)
        }

        dato = json_message_maker(SensorTypes.RESERVOIR, str(timestamp), [reading], self._sensor_name,
                                  self._coordinates)

        return dato
