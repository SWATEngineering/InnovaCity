import threading
import time
import json
import random
from datetime import datetime
from datetime import timedelta

from .Simulator import Simulator
from ..Writers import Writer


class RainSimulator(Simulator):
    __count = 0  # Class variable to name the sensor
    __rain_intensity = 0  # Class variable for rain intensity
    __rain_lock = None

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        RainSimulator.__count += 1
        super().__init__(writer, latitude, longitude,
                         f"Sensore di Pioggia {RainSimulator.__count}", frequency_in_s)
        RainSimulator.__rain_lock = threading.Lock()

    def set_rain_intensity(self, intensity: int) -> None:
        RainSimulator.__rain_intensity = intensity

    def get_rain_intensity(self) -> int:
        return RainSimulator.__rain_intensity

    def generate_value(self, intensity: int) -> float:
        if (intensity == 0):
            return 0.0
        else:
            base_value = 0.5
            random_factor = random.uniform(0.9, 1.1)
            rainfall_value = base_value * random_factor * intensity**2
            return rainfall_value

    def try_initiate_rain(self):
        if random.random() < 1 / (24 * 3600 / self.get_frequency_is_s()):
            self.set_rain_intensity(random.randint(1, 5))
            print(f"initiated {self.get_sensor_name()}")

    def try_stop_rain(self):
        if random.random() < 1 / (24 * 3600 / self.get_frequency_is_s()):
            self.set_rain_intensity(0)
            print(f"stopped {self.get_sensor_name()}", flush=True)

    def generate_non_real_time_data(self):
        last_timestamp = datetime.timestamp(
            datetime.now()) + 60 * self.get_frequency_is_s()
        iter_timestamp = last_timestamp
        first_timestamp = last_timestamp - 86400

        data_to_insert = []

        while (iter_timestamp > first_timestamp):
            with RainSimulator.__rain_lock:
                if self.get_rain_intensity() == 0:
                    self.try_initiate_rain()
                else:
                    self.try_stop_rain()

            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(self.generate_value(self.get_rain_intensity())),
                "type": "RainSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }
            data_to_insert.append(dato)
            iter_timestamp -= super().get_frequency_is_s()
            time.sleep(0)

        batch_size = 5000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            super().get_writer().write(json.dumps(batch))
        time.sleep(max(0, (last_timestamp + self.get_frequency_is_s() -
                   datetime.timestamp(datetime.now()))))

    def simulate(self) -> None:
        self.generate_non_real_time_data()
        print(datetime.now())
        while super().continue_simulating():
            with RainSimulator.__rain_lock:
                if self.get_rain_intensity() == 0:
                    self.try_initiate_rain()
                else:
                    self.try_stop_rain()

            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(self.generate_value(self.get_rain_intensity())),
                "type": "RainSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }

            super().get_writer().write(json.dumps(dato))
            time.sleep(super().get_frequency_is_s())
