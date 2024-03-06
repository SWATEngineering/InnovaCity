from sensor_simulator_strategy import SensorSimulatorStrategy
import math
from ..utils.sensor_types import SensorTypes
from  ..utils.json_message_maker import json_message_maker
import time

class HumiditySensorSensorSimulator(SensorSimulatorStrategy):
    
     
    __phase: float=0.2  # Imposta lo spostamento di fase per allineare il picco di umidità con le ore del mattino
    __amplitude: float
    __percen: float
    
    def __init__(self):
        super().__init__()
        self.__amplitude=self._calculate_ampiezza()
    
    def _calculate_ampiezza(self):
        
            
        current_month = self._datetime_obj.now().month
        if 3 <= current_month <= 5:  # Primavera: da marzo a maggio
                return 0.45
        elif 6 <= current_month <= 8:  # Estate: da giugno a agosto
                return 0.3
        elif 9 <= current_month <= 11:  # Autunno: da settembre a novembre
                return 0.65
        else:  # Inverno: da dicembre a febbraio
                return 0.85

    def _calcola_percentuale(self) -> float:
        timestamp=self._datetime_obj.now()
        hours = (timestamp % 86400) / 3600
        relative_humidity = (math.sin(2 * math.pi * (hours - self.__phase) / 24) * self.__amplitude + 1) / 2
        relative_humidity += self._random_obj.uniform(-0.01, 0.01)
        relative_humidity = max(0, min(1, relative_humidity))
        percentuale = relative_humidity * (100 - 35) + 35
        return percentuale
    
    def simulate(self) -> str:
                      
        timestamp = self._datetime_obj.now()
        self.__percen = self._calcola_percentuale()
    
        reading = {
                "type": "%",
                "value": round(self.__percen,2)
        }
    
        dato = json_message_maker(SensorTypes.HUMIDITY, str(timestamp), reading, self._sensor_name, self._coordinates)
    
        time.sleep(self._wait_time_in_seconds.total_seconds())
    
        return dato
