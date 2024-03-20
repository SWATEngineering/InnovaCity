import math
from datetime import datetime
from random import Random
from typing import Type

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy

from src.utils.json_message_maker import json_message_maker
from src.utils.sensor_types import SensorTypes
from src.utils.coordinates import Coordinates


class TemperatureSensorSensorSimulator(SensorSimulatorStrategy):
    __calibration = None

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self.__calibration = self._random_obj.uniform(-0.5, 0.5)

    def simulate(self) -> str:
        now = self._datetime_obj.now()
        hours = (int(now.timestamp()) % 86400) / 3600

        simulated_value = ((
            math.cos(
                math.pi * ((hours - 12) / 12)
                # in questo modo il periodo [-1,1] basta per raggiungere i periodi
            ) + 1) / 2
           # in questo modo spostiamo il coseno tutto in positivo, con valori che vanno da 0 a 1
        ) * 12 + 5 + self.__calibration + self._random_obj.random()
        # per temperature che vanno da 5 a 17 gradi a fronte della fottore di calibrazione

        reading = {
            "type": "Celsius Degrees",
            "value": round(simulated_value, 2)
        }

        dato = json_message_maker(SensorTypes.TEMPERATURE, str(now), [reading], self._sensor_name, self._coordinates)

        return dato
