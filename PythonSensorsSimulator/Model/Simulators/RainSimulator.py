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
        return math.sin(angle) * intensity**2 * random_factor


class RainSimulator(Simulator):
    __rain_intensity = None
    __rain_duration = None
    __second_rain_left = None

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        super().__init__(writer, latitude, longitude, "Pluviometro", frequency_in_s)
        self.__rain_intensity = 0
        self.__rain_duration = 0
        self.__second_rain_left = 0

    def set_rain_intensity(self, intensity: int) -> None:
        self.__rain_intensity = intensity

    def get_rain_intensity(self) -> int:
        return self.__rain_intensity

    def set_rain_duration(self, duration: int) -> None:
        self.__rain_duration = duration

    def get_rain_duration(self) -> int:
        return self.__rain_duration

    def set_second_rain_left(self, second_left: int) -> None:
        self.__second_rain_left = second_left

    def get_second_rain_left(self) -> int:
        return self.__second_rain_left

    def try_initiate_rain(self):
        if random.random() < 1 / (3 * 3600 / self.get_frequency_in_s()):
            self.set_rain_intensity(random.randint(1, 5))
            self.set_rain_duration(random.randint(7200, 14000))
            self.set_second_rain_left(self.get_rain_duration())

    def stop_rain(self):
        self.set_rain_intensity(0)
        self.set_rain_duration(0)
        self.set_second_rain_left(0)

    def insert_not_real_time_data(self) -> None:

        last_timestamp = datetime.timestamp(
            datetime.now()) + 20 * super().get_frequency_in_s()
        iter_timestamp = last_timestamp
        first_timestamp = last_timestamp - 86400

        data_to_insert = []

        while iter_timestamp > first_timestamp:
            if self.get_rain_intensity() == 0:
                self.try_initiate_rain()

            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(
                    generate_value(self.get_rain_intensity(), self.get_rain_duration(), self.get_second_rain_left())),
                "type": "RainSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }

            self.set_second_rain_left(
                self.get_second_rain_left() - super().get_frequency_in_s())
            if self.get_second_rain_left() == 1:
                self.stop_rain()

            data_to_insert.append(dato)
            iter_timestamp -= super().get_frequency_in_s()

        batch_size = 5000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            super().get_writer().write(json.dumps(batch))
        self.stop_rain()
        time.sleep(max(0, (last_timestamp + super().get_frequency_in_s() -
                           datetime.timestamp(datetime.now()))))

    def simulate(self) -> None:
        self.insert_not_real_time_data()
        while super().continue_simulating():
            if self.get_rain_intensity() == 0:
                self.try_initiate_rain()

            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(
                    generate_value(self.get_rain_intensity(), self.get_rain_duration(), self.get_second_rain_left())),
                "type": "RainSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }

            self.set_second_rain_left(
                self.get_second_rain_left() - super().get_frequency_in_s())
            if self.get_second_rain_left() == 1:
                self.stop_rain()

            super().get_writer().write(json.dumps(dato))
            time.sleep(super().get_frequency_in_s())
