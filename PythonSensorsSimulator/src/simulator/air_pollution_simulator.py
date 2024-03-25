from datetime import datetime
from typing import Type
from random import Random
import math

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
from src.utils.coordinates import Coordinates

class AirPollutionSensorSimulator(SensorSimulatorStrategy):
    __value: float  # value read by the sensor
    __base_value: float = 5
    __month: int
    __hour: int

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name,random_obj,datetime_obj,coordinates)
        self.__month = self._datetime_obj.now().month
        self.__hour = self._datetime_obj.now().hour

    # Calculate seasonal variation using a sinusoidal function
    def __calculate_seasonal_variation(self) -> float:
        # The result varies between -10 and 10
        return math.sin(2 * math.pi * (self.__month - 1) / 12) * 10
        # -1 because month is between 1 and 12 and we want it starting from 0

    # Sinusoidal function to model daily variations in pollution levels
    def __calculate_time_variation(self) -> float:
        # The result peaks around 18:00
        time_variation = math.sin((self.__hour - 6) * (math.pi / 12))
        return time_variation

    # generate air pollution value
    def __generate_air_pollution(self) -> float:
        seasonal_variation = self.__calculate_seasonal_variation()

        time_variation = self.__calculate_time_variation()

        value = self.__base_value + seasonal_variation + time_variation + self._random_obj.uniform(-2, 2)

        return value

    def simulate(self) -> str:
        timestamp = self._datetime_obj.now()
        self.__value = self.__generate_air_pollution()

        reading = {
            "type": "micro-g/mc",
            "value": round(self.__value, 2)
        }

        dato = json_message_maker(SensorTypes.AIR_POLLUTION, str(timestamp), [reading], self._sensor_name,
                                  self._coordinates)

        return dato