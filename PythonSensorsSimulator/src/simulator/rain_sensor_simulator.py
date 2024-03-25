import math
from datetime import datetime, timedelta
from random import Random
from typing import Type

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
from src.utils.coordinates import Coordinates


class RainSensorSensorSimulator(SensorSimulatorStrategy):
    __rain_intensity: int
    __rain_start_time: datetime
    __rain_end_time: datetime

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self.__rain_intensity = 0
        # Start the rain between 0 and 1 hour from the simulator's start
        self.__rain_start_time = self._datetime_obj.now(
        ) + timedelta(seconds=self._random_obj.randint(0, 3600))
        self.__rain_end_time = None

    def __generate_value(self) -> float:
        if self.__rain_intensity == 0:
            return 0.0
        else:
            time_difference = self._datetime_obj.now() - self.__rain_start_time
            time_passed = time_difference.total_seconds()
            total_time_datetime = self.__rain_end_time - self.__rain_start_time
            total_time = total_time_datetime.total_seconds()
            angle = (time_passed / total_time) * math.pi
            random_factor = 1.0 + self._random_obj.uniform(-0.1, 0.1)
            return math.sin(angle) * (self.__rain_intensity**2) * random_factor

    def __initiate_rain(self):
        self.__rain_intensity = self._random_obj.randint(1, 5)
        # Set the initial rain duration
        rain_duration = self._random_obj.randint(7200, 14000)
        self.__rain_end_time = self.__rain_start_time + \
            timedelta(seconds=rain_duration)

    def __stop_rain(self):
        self.__rain_intensity = 0
        self.__rain_end_time = None
        not_rain_duration = self._random_obj.randint(14000, 28000)
        self.__rain_start_time = self._datetime_obj.now(
        ) + timedelta(seconds=not_rain_duration)

    def simulate(self) -> str:
        if self.__rain_intensity == 0 and self._datetime_obj.now() >= self.__rain_start_time:
            self.__initiate_rain()

        if self.__rain_end_time and self._datetime_obj.now() >= self.__rain_end_time:
            self.__stop_rain()

        reading = {
            "type": "mm/mc",
            "value": round(self.__generate_value(), 2)
        }

        data = json_message_maker(
            SensorTypes.RAIN,
            str(self._datetime_obj.now()),
            [reading],
            self._sensor_name,
            self._coordinates
        )

        return data
