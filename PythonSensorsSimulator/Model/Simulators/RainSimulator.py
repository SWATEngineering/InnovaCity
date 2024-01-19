import math
import time
import json
import random
from datetime import datetime

from .Simulator import Simulator
from ..Writers import Writer


def generate_value(intensity: int, duration: int, second_left: int) -> float:
    if intensity == 0:
        return 0.0
    else:
        angle = ((second_left /
                 duration)) * math.pi
        random_factor = 1.0 + random.uniform(-0.1, 0.1)
        return math.sin(angle) * intensity * random_factor


class RainSimulator(Simulator):
    __rain_intensity = None
    __rain_duration = None
    __second_rain_left = None

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        super().__init__(writer, latitude, longitude, "Pluviometro", frequency_in_s)
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def try_initiate_rain(self):
        if random.random() < 1 / (3 * 3600 / super()._frequency_in_s):
            self.__rain_intensity = random.randint(1, 5)
            self.__rain_duration = random.randint(7200, 14000)
            self.__second_rain_left = self.__rain_duration

    def stop_rain(self):
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def insert_not_real_time_data(self) -> None:

        last_timestamp = datetime.timestamp(
            datetime.now()) + 20 * super()._frequency_in_s
        iter_timestamp = last_timestamp
        first_timestamp = last_timestamp - 86400

        data_to_insert = []

        while iter_timestamp > first_timestamp:
            if self.__rain_intensity == 0:
                self.try_initiate_rain()

            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(
                    generate_value(self.__rain_intensity, self.__rain_duration, self.__second_rain_left)),
                "type": "RainSimulator",
                "latitude": super()._latitude,
                "longitude": super()._longitude,
                "nome_sensore": super()._sensor_name
            }

            self.__second_rain_left = self.__second_rain_left - super()._frequency_in_s
            if self.__second_rain_left == 1:
                self.stop_rain()

            data_to_insert.append(dato)
            iter_timestamp -= super()._frequency_in_s

        batch_size = 5000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            super()._writer.write(json.dumps(batch))
        self.stop_rain()
        time.sleep(max(0, int(last_timestamp + super()._frequency_in_s - datetime.timestamp(datetime.now()))))

    def simulate(self) -> None:
        self.insert_not_real_time_data()
        while super().continue_simulating():
            if self.__rain_intensity == 0:
                self.try_initiate_rain()

            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(
                    generate_value(self.__rain_intensity, self.__rain_duration, self.__second_rain_left)),
                "type": "RainSimulator",
                "latitude": super()._latitude,
                "longitude": super()._longitude,
                "nome_sensore": super()._sensor_name
            }

            self.__second_rain_left = self.__second_rain_left - super()._frequency_in_s
            if self.__second_rain_left() == 1:
                self.stop_rain()

            super()._writer.write(json.dumps(dato))
            time.sleep(super()._frequency_in_s)
