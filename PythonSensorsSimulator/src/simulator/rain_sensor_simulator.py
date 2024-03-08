import math

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker


class RainSensorSensorSimulator(SensorSimulatorStrategy):
    __rain_intensity: int
    __rain_duration: int
    __second_rain_left: int
    # TODO
    # frequency_in_s = wait_time_in_seconds dentro a SimulatorThread
    # per il momento assumeremo che sia sempre di un secondo
    __frequency_in_s = 1

    def __init__(self, **data):
        super().__init__(**data)
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def __generate_value(self) -> float:
        if self.__rain_intensity == 0:
            return 0.0
        else:
            angle = ((self.__second_rain_left /
                      self.__rain_duration)) * math.pi
            random_factor = 1.0 + self._random_obj.uniform(-0.1, 0.1)
            return math.sin(angle) * self.__rain_intensity * random_factor

    def __try_initiate_rain(self):
        if self._random_obj.random() < 1 / (3 * 3600 / self.__frequency_in_s):
            self.__rain_intensity = self._random_obj.randint(1, 5)
            self.__rain_duration = self._random_obj.randint(7200, 14000)
            self.__second_rain_left = self.__rain_duration

    def __stop_rain(self):
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def simulate(self) -> str:
        now = self._datetime_obj.now()

        if self.__rain_intensity == 0:
            self.__try_initiate_rain()

        self.__second_rain_left = self.__second_rain_left - self.__frequency_in_s
        if self.__second_rain_left == 1:
            self.__stop_rain()

        reading = {
            "type": "mm/mc",
            "value": round(self.__generate_value(), 2)
        }

        dato = json_message_maker(
            SensorTypes.RAIN,
            str(now),
            [reading],
            self._sensor_name,
            self._coordinates
        )

        return dato
