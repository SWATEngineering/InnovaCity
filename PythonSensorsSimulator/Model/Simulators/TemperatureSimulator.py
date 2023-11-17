import time

from PythonSensorsSimulator.Model.Simulators.Simulator import Simulator
from PythonSensorsSimulator.Model.Writers.Writer import Writer
from datetime import datetime
import json
import math
import random


class TemperatureSimulator(Simulator):

    def __init__(self, writer: Writer, id: str, frequency_in_s: int = 1):
        super().__init__(writer, id, frequency_in_s)

    def simulate(self) -> None:
        while self.continue_simulating:
            hours = (datetime.timestamp(datetime.now()) % 86400) / 3600
            sym_temperature = math.sin(
                (hours - 12 ) / 12
            ) * 12 + 5 + random.random()*0.2 # per temperature che vanno da 5 a 17 gradi
            dato = {
                "timestamp": datetime.timestamp(datetime.now()),
                "value": sym_temperature,
                "type": "TemperatureSimulator",
                "id": self.id
            }
            self.writer.write(json.dumps(dato, indent=2))
            time.sleep(self.frequency_in_s)
