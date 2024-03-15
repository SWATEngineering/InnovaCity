from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
import math

class TrafficSensorSimulator(SensorSimulatorStrategy):
    __num_cars: int
    __average_time: float
    __base_time: float
    __traffic_level: str

    __LOW_THRESHOLD = 7
    __MEDIUM_THRESHOLD = 15
    __HIGH_THRESHOLD = 30

    def __init__(self, **data):
        super().__init__(**data)
        self.__num_cars = self._random_obj.uniform(5, 10)
        self.__base_time = 5

    def _update_num_cars(self):
        self.__num_cars += self._random_obj.uniform(-0.5, 0.5)

    def _update_average_time(self):
        self.__average_time = self.__base_time + self._random_obj.uniform(-0.5, 0.5)  + math.sqrt(self._get_datetime_factor() * self.__num_cars)
        # check if average time is too low
        if self.__average_time < self.__base_time:
            self.__average_time = self.__base_time

    def _get_datetime_factor(self) -> float:
        factor: int
        hour = self._datetime_obj.now().hour
        day = self._datetime_obj.now().weekday()

        if 0 <= day <= 6 and  (6 <= hour <= 9 or 16 <= hour <= 19):     # rush hour
            factor = 2
        elif 0 <= day <= 6 and (9 < hour < 16 or 19 < hour < 24):       # week day
            factor = 1.5
        else:                                                           # night and sunday
            factor = 1

        return factor

    def _update_traffic_level(self):
        if self.__num_cars <= self.__LOW_THRESHOLD:
            self.__traffic_level = "LOW"
        elif self.__LOW_THRESHOLD < self.__num_cars <= self.__MEDIUM_THRESHOLD:
            self.__traffic_level = "MEDIUM"
        elif self.__MEDIUM_THRESHOLD < self.__num_cars <= self.__HIGH_THRESHOLD:
            self.__traffic_level = "HIGH"
        else:
            self.__traffic_level = "BLOCKED"

    def simulate(self) -> str:
        timestamp = self._datetime_obj.now()

        self._update_num_cars()
        self._update_average_time()
        self._update_traffic_level()

        reading1 = {
            "type": "Number",
            "value": self.__num_cars
        }

        reading2 = {
            "type": "level",
            "value": self.__traffic_level
        }

        reading3 = {
            "type": "km/h",
            "value": self.__average_time
        }

        dato = json_message_maker(SensorTypes.TRAFFIC, str(timestamp), [reading1, reading2, reading3], self._sensor_name,
                                  self._coordinates)

        return dato