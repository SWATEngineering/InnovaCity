from datetime import datetime
from random import Random
from typing import Type

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
import math
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
from src.utils.coordinates import Coordinates


class EcoZoneSensorSensorSimulator(SensorSimulatorStrategy):
    __tasso_massimo: float
    __svuotamento: int
    __inizio: int
    __percentuale: float
    __tasso_notturno: float = 0.001

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self.__tasso_massimo = self._random_obj.uniform(0.25, 0.75)
        self.__svuotamento = self._random_obj.randint(20, 23)
        self.__inizio = self._random_obj.randint(1, 6)

    def _calcolo_tasso(self, hours) -> float:

        if self.__inizio <= hours <= self.__svuotamento:
            tasso_riempimento = (hours - self.__inizio) / (self.__svuotamento - self.__inizio) * self.__tasso_massimo
        else:
            tasso_riempimento = (24 - hours + self.__inizio) / 24 * self.__tasso_notturno

        tasso_riempimento = max(0, min(1, tasso_riempimento))

        return tasso_riempimento

    def _calcolo_percentuale(self) -> float:

        now = self._datetime_obj.now()
        hours = (int(now.timestamp()) % 86400) / 3600
        tasso_riempimento = self._calcolo_tasso(hours)
        tasso_riempimento += self._random_obj.uniform(-0.001, 0.001)
        oscillazione = self._random_obj.uniform(-0.001, 0.001)
        self.__percentuale = tasso_riempimento * 100 + oscillazione
        return self.__percentuale

    def simulate(self) -> str:

        timestamp = self._datetime_obj.now()
        self.__percentuale = self._calcolo_percentuale()

        reading = {
            "type": "%",
            "value": round(self.__percentuale, 2)
        }

        dato = json_message_maker(SensorTypes.ECO_ZONE, str(timestamp), [reading], self._sensor_name, self._coordinates)

        return dato
