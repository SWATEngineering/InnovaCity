import time
import json
import math
import random
from datetime import datetime

from .Simulator import Simulator
from ..Writers import Writer


class TemperatureSimulator(Simulator):
    __count = 0

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        TemperatureSimulator.__count += 1
        super().__init__(writer, latitude, longitude,
                         f"Sensore di Temperatura {TemperatureSimulator.__count}", frequency_in_s)

    def simulate(self) -> None:
        while super().continue_simulating():
            hours = (datetime.timestamp(datetime.now()) % 86400) / 3600
            sym_temperature = ((
                math.cos(
                    math.pi * ((hours - 12) / 12)
                    # in questo modo il periodo [-1,1] basta per raggiungere i periodi
                ) + 1) / 2
                # in questo modo spostiamo il coseno tutto in positivo, con valori che vanno da 0 a 1
            ) * 12 + 5 + random.random()  # per temperature che vanno da 5 a 17 gradi
            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(sym_temperature),
                "type": "TemperatureSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }
            super().get_writer().write(json.dumps(dato))
            time.sleep(super().get_frequency_is_s())
