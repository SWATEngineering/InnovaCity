import math
import time
import json
import random
from datetime import datetime
from datetime import timedelta

from .Simulator import Simulator
from ..Writers import Writer


class RainSimulator(Simulator):
    __count = 0  # Class variable to name the sensor
    __rain_intensity = 0
    __rain_duration = 0
    __second_rain_left = 0

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        RainSimulator.__count += 1
        super().__init__(writer, latitude, longitude,
                         f"Pluviometro {RainSimulator.__count}", frequency_in_s)

    #
    def set_rain_intensity(self, intensity: int) -> None:
        RainSimulator.__rain_intensity = intensity

    def get_rain_intensity(self) -> int:
        return RainSimulator.__rain_intensity

    #
    def set_rain_duration(self, duration: int) -> None:
        RainSimulator.__rain_duration = duration

    def get_rain_duration(self) -> int:
        return RainSimulator.__rain_duration

    #
    def set_second_rain_left(self, second_left: int) -> None:
        RainSimulator.__second_rain_left = second_left

    def get_second_rain_left(self) -> int:
        return RainSimulator.__second_rain_left

    def try_initiate_rain(self):
        if random.random() < 1 / (12 * 10 / self.get_frequency_is_s()):
            self.set_rain_intensity(random.randint(1, 5))
            self.set_rain_duration(random.randint(72000, 140000))
            self.set_second_rain_left(self.get_rain_duration())

    def stop_rain(self):
        self.set_rain_intensity(0)
        self.set_rain_duration(0)
        self.set_second_rain_left(0)

    def generate_value(self) -> float:
        if (self.get_rain_intensity() == 0):
            return 0.0
        else:
            angle = ((self.get_second_rain_left() /
                     self.get_rain_duration()) * math.pi)
            return math.sin(angle) * self.get_rain_intensity()**3

    def insert_not_real_time_data(self) -> None:  # è da cambaire

        last_timestamp = datetime.timestamp(
            datetime.now()) + 40 * super().get_frequency_is_s()
        iter_timestamp = last_timestamp
        first_timestamp = last_timestamp - 86400

        data_to_insert = []

        while (iter_timestamp > first_timestamp):
            if super().get_sensor_name() == "Pluviometro 1":
                self.try_initiate_rain()

            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(self.generate_value()),
                "type": "RainSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }

            if super().get_sensor_name() == "Pluviometro 1":
                self.set_second_rain_left(
                    self.get_second_rain_left() - super().get_frequency_is_s())
                if self.get_second_rain_left() == 0:
                    self.stop_rain()
            time.sleep(0)

        batch_size = 5000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            super().get_writer().write(json.dumps(batch))
        time.sleep(max(0, (last_timestamp + super().get_frequency_is_s() -
                   datetime.timestamp(datetime.now()))))

    def simulate(self) -> None:

        while super().continue_simulating():
            if super().get_sensor_name() == "Pluviometro 1":
                self.try_initiate_rain()

            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(self.generate_value()),
                "type": "RainSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }

            if super().get_sensor_name() == "Pluviometro 1":
                self.set_second_rain_left(
                    self.get_second_rain_left() - super().get_frequency_is_s())
                if self.get_second_rain_left() == 0:
                    self.stop_rain()
            super().get_writer().write(json.dumps(dato))
            time.sleep(super().get_frequency_is_s())
