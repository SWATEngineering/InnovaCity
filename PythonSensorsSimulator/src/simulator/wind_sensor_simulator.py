import math
from datetime import datetime
from random import Random
from typing import Type

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.json_message_maker import json_message_maker
from src.utils.sensor_types import SensorTypes
from src.utils.coordinates import Coordinates


class WindSensorSensorSimulator(SensorSimulatorStrategy):
    __direction: int = 0
    __speed: float = 0

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)

    def simulate(self) -> str:

        if self.__speed == 0:
            self.__speed = self._random_obj.random() * 6 + 2
            self.__direction = int(self._random_obj.random() * 365)

        def normal_distribution(x: float, sigma: float, mu: float) -> float:
            return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(
                -0.5 * ((x - mu) / sigma) ** 2
            )

        multiplying_factor = self._random_obj.random() * 0.1

        move_sx = self._random_obj.random() * multiplying_factor
        move_dx = self._random_obj.random() * multiplying_factor
        prob_sx = normal_distribution(self.__speed - move_sx, 0.8, 4.5)
        prob_dx = normal_distribution(self.__speed + move_dx, 0.8, 4.5)
        decisor = self._random_obj.random() * (prob_dx + prob_sx)

        self.__speed = self.__speed - move_sx if prob_sx > decisor else self.__speed + move_dx
        self.__direction += (self._random_obj.random() * 4 - 2) % 360

        return json_message_maker(SensorTypes.WIND, str(self._datetime_obj.now()), [
            {
                "type": "km/h",
                "value": "{0:.2f}".format(self.__speed)
            },
            {
                "type": "direction",
                "value": self.__direction
            }
        ], self._sensor_name, self._coordinates)
