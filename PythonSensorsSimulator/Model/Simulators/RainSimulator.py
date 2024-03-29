import math
import time
import json
import random
from datetime import datetime

from .Simulator import Simulator
from ..Writers import Writer


class RainSimulator(Simulator):
    __rain_intensity: int
    __rain_duration: int
    __second_rain_left: int

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        super().__init__(writer, latitude, longitude, "Pluviometro", frequency_in_s)
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def __generate_value(self) -> float:
        if self.__rain_intensity == 0:
            return 0.0
        else:
            angle = ((self.__second_rain_left /
                      self.__rain_duration)) * math.pi
            random_factor = 1.0 + random.uniform(-0.1, 0.1)
            return math.sin(angle) * self.__rain_intensity * random_factor

    def __try_initiate_rain(self):
        if random.random() < 1 / (3 * 3600 / self._frequency_in_s):
            self.__rain_intensity = random.randint(1, 5)
            self.__rain_duration = random.randint(7200, 14000)
            self.__second_rain_left = self.__rain_duration

    def __stop_rain(self):
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def _insert_not_real_time_data(self) -> None:
        last_timestamp = datetime.timestamp(
            datetime.now()) + 20 * self._frequency_in_s
        iter_timestamp = last_timestamp
        first_timestamp = last_timestamp - 86400

        data_to_insert = []

        while iter_timestamp > first_timestamp:
            if self.__rain_intensity == 0:
                self.__try_initiate_rain()

            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(
                    self.__generate_value()),
                "type": "RainSimulator",
                "latitude": self._latitude,
                "longitude": self._longitude,
                "nome_sensore": self._sensor_name
            }

            self.__second_rain_left = self.__second_rain_left - self._frequency_in_s
            if self.__second_rain_left == 1:
                self.__stop_rain()

            data_to_insert.append(dato)
            iter_timestamp -= self._frequency_in_s

        batch_size = 5000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            self._writer.write(json.dumps(batch))
        self.__stop_rain()
        time.sleep(max(0, int(last_timestamp + self._frequency_in_s - datetime.timestamp(datetime.now()))))

    def simulate(self) -> None:
        self._insert_not_real_time_data()
        while super().continue_simulating():
            if self.__rain_intensity == 0:
                self.__try_initiate_rain()

            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(
                    self.__generate_value()),
                "type": "RainSimulator",
                "latitude": self._latitude,
                "longitude": self._longitude,
                "nome_sensore": self._sensor_name
            }

            self.__second_rain_left = self.__second_rain_left - self._frequency_in_s
            if self.__second_rain_left == 1:
                self.__stop_rain()

            self._writer.write(json.dumps(dato))
            time.sleep(self._frequency_in_s)
