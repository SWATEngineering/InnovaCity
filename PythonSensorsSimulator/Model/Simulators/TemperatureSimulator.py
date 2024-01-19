import time
import json
import math
import random
from datetime import datetime

from .Simulator import Simulator
from ..Writers import Writer


class TemperatureSimulator(Simulator):
    __count = 0
    __calibration = None

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        TemperatureSimulator.__count += 1
        self.__calibration = random.uniform(-0.5, 0.5)
        # fattore di calibrazione necessario a garantire un maggiore varianza nei dati simulati dai sensori
        super().__init__(writer, latitude, longitude,
                         f"Sensore di Temperatura {TemperatureSimulator.__count}", frequency_in_s)

    def insert_not_real_time_data(self) -> None:

        last_timestamp = datetime.timestamp(datetime.now()) + 20 * self._frequency_in_s
        iter_timestamp = last_timestamp
        first_timestamp = last_timestamp - 86400

        data_to_insert = []

        while iter_timestamp > first_timestamp:

            hours = (iter_timestamp % 86400) / 3600
            sym_temperature = ((math.cos(math.pi * ((hours - 12) / 12)) + 1) / 2) * \
                12 + 5 + self.__calibration + random.random()

            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(sym_temperature),
                "type": "TemperatureSimulator",
                "latitude": self._latitude,
                "longitude": self._longitude,
                "nome_sensore": self._sensor_name
            }

            data_to_insert.append(dato)
            iter_timestamp -= self._frequency_in_s

        batch_size = 5000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            self._writer.write(json.dumps(batch))
        time.sleep(max(0, int(last_timestamp + self._frequency_in_s - datetime.timestamp(datetime.now()))))

        # l'effettiva simulazione (dati generati real time e mandati a kakfa singolarmente) parte poco dopo

    def simulate(self) -> None:
        self.insert_not_real_time_data()  # strettamente per il poc
        while super().continue_simulating():

            hours = (datetime.timestamp(datetime.now()) % 86400) / 3600

            sym_temperature = ((
                math.cos(
                    math.pi * ((hours - 12) / 12)
                    # in questo modo il periodo [-1,1] basta per raggiungere i periodi
                ) + 1) / 2
                # in questo modo spostiamo il coseno tutto in positivo, con valori che vanno da 0 a 1
            ) * 12 + 5 + self.__calibration + random.random()
            # per temperature che vanno da 5 a 17 gradi a fronte della fottore di calibrazione

            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(sym_temperature),
                "type": "TemperatureSimulator",
                "latitude": self._latitude,
                "longitude": self._longitude,
                "nome_sensore": self._sensor_name
            }
            self._writer.write(json.dumps(dato))
            time.sleep(self._frequency_in_s)
