from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
import json
import math
import time

class ReservoirSensorSimulator(SensorSimulatorStrategy):

    __reservoir_percentage: float

    def __init__(self):
        super().__init__()
        self.__reservoir_percentage = 95.0

    def calculate_evaporation_rate(self, hour, month):
        base_evaporation_rate = ((math.cos(math.pi * ((hour - 12) / 12)) + 1) / 2) * 0.4 + 0.3
        
        if 3 <= month < 6: 
            base_evaporation_rate += 0.2
        elif 6 <= month < 9:
            base_evaporation_rate += 0.4
        elif 9 <= month < 12:
            base_evaporation_rate -= 0.1
        else:
            base_evaporation_rate -= 0.2
        
        evaporation_rate = base_evaporation_rate + self.__random_obj.uniform(-0.05, 0.05)
        evaporation_rate = max(0, min(1, evaporation_rate))
        
        return evaporation_rate

    def measure_reservoir_level(self):
        current_time = self.__datetime_obj.now()
        hour = current_time.hour
        month = current_time.month
        
        evaporation_rate = self.calculate_evaporation_rate(hour, month)
        evaporation_change = self.__random_obj.uniform(-0.1, 0.1) * evaporation_rate
        total_change = self.__random_obj.uniform(-0.1, 0.1) + evaporation_change
        
        self.__reservoir_percentage = max(0, min(100, self.__reservoir_percentage + total_change))
        
        return self.__reservoir_percentage

    def simulate(self) -> str:
        json_data = ""

        while super().continue_simulating():

            hours = (self.__datetime_obj.timestamp(self.__datetime_obj.now()) % 86400) / 3600
            res_level = self.measure_reservoir_level()

            dato = {
                "timestamp": str(self.__datetime_obj.now()),
                "value": "{:.2f}".format(res_level),
                "type": "reservoir",
                "latitude": self._latitude,
                "longitude": self._longitude,
                "nome_sensore": self._sensor_name
            }
            json_data += json.dumps(dato) + "\n"
            time.sleep(self._frequency_in_s)

        return json_data