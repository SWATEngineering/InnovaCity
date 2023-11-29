import time

from .Simulator import Simulator
from ..Writers import Writer
from datetime import datetime, timezone
import json
import math
import random


class TemperatureSimulator(Simulator):

    def __init__(self, writer: Writer, id: str, frequency_in_s: int = 1):
        super().__init__(writer, id, frequency_in_s)

    def simulate(self) -> None:
        while self._Simulator__continue_simulating:
            hours = (datetime.timestamp(datetime.now()) % 86400) / 3600
            sym_temperature = ((
                                       math.cos(
                                           math.pi * ((hours - 12) / 12)
                                           # in questo modo il periodo [-1,1] basta per raggiungere i periodi
                                       ) + 1) / 2
                               # in questo modo spostiamo il coseno tutto in positivo, con valori che vanno da 0 a 1
                               ) * 12 + 5 + random.random() * 0.2  # per temperature che vanno da 5 a 17 gradi
            dato = {
                "timestamp": str(datetime.now()),
                "value": "{:.2f}".format(sym_temperature),
                "type": "TemperatureSimulator",
                "id": self._Simulator__id
            }
            self._Simulator__writer.write(json.dumps(dato))
            time.sleep(self._Simulator__frequency_in_s)
