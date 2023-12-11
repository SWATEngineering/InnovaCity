import time
import json
import math
import random
from datetime import datetime
from datetime import timedelta


from .Simulator import Simulator
from ..Writers import Writer


class TemperatureSimulator(Simulator):
    __count = 0
    ##
    __calibration = None
    __initial_timestamp = None
    ##

    def __init__(self, writer: Writer, latitude: float, longitude: float, frequency_in_s: int = 1):
        TemperatureSimulator.__count += 1
        self.__calibration = random.uniform(-0.5, 0.5)
        # fattore di calibrazione necessario a garantire un maggiore varianza nei dati simulati dai sensori
        super().__init__(writer, latitude, longitude,
                         f"Sensore di Temperatura {TemperatureSimulator.__count}", frequency_in_s)
        self.insert_not_real_time_data()
    ##

    def get_calibration(self) -> float:
        return self.__calibration

    def insert_not_real_time_data(self) -> None:
        iter_timestamp = datetime.timestamp(datetime.now())
        primo_timestamp = iter_timestamp - 86400
        data_to_insert = []

        while (iter_timestamp > primo_timestamp):
            iter_timestamp -= super().get_frequency_is_s()
            hours = (iter_timestamp % 86400) / 3600
            sym_temperature = ((
                math.cos(
                    math.pi * ((hours - 12) / 12)
                    # in questo modo il periodo [-1,1] basta per raggiungere i periodi
                ) + 1) / 2
                # in questo modo spostiamo il coseno tutto in positivo, con valori che vanno da 0 a 1
            ) * 12 + 5 + self.get_calibration() + random.random()
            # per temperature che vanno da 5 a 17 gradi a fronte della fottore di calibrazione
            dato = {
                "timestamp": str(datetime.fromtimestamp(iter_timestamp)),
                "value": "{:.2f}".format(sym_temperature),
                "type": "TemperatureSimulator",
                "latitude": super().get_latitude(),
                "longitude": super().get_longitude(),
                "nome_sensore": super().get_sensor_name()
            }

            data_to_insert.append(dato)

        batch_size = 1000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            super().get_writer().write(json.dumps(batch))

    def simulate(self) -> None:
        while super().continue_simulating():

            hours = (datetime.timestamp(datetime.now()) % 86400) / 3600

            sym_temperature = ((
                math.cos(
                    math.pi * ((hours - 12) / 12)
                    # in questo modo il periodo [-1,1] basta per raggiungere i periodi
                ) + 1) / 2
                # in questo modo spostiamo il coseno tutto in positivo, con valori che vanno da 0 a 1
            ) * 12 + 5 + self.get_calibration() + random.random()
            # per temperature che vanno da 5 a 17 gradi a fronte della fottore di calibrazione

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
