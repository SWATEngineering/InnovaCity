from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker

class AirPollutionSensorSimulator(SensorSimulatorStrategy):
    
    value: float # value read by the sensor
    base_value: float = 10
    variation_min: float = -5
    variation_max: float = 5

    def __init__(self, **data):
        super().__init__(**data)

    # return the variation percentage based on the season
    def _get_seasonal_variation(self) -> float:
        
        month = self.__date_time.now().month
        
        if month in [12, 1, 2]: #winter
            # air pollution is higher due to the heating
            return 20 #% added
        elif month in [3, 4, 5]: #spring
            return 5 #%
        elif month in [6, 7, 8]: #summer
            return 0 #%
        elif month in [9, 10, 11]: #autumn
            return 5 #%
        else:
            print("Error: month not valid")
            exit(1)

    # generate air pollution value
    def _generate_air_pollution(self) -> float:

        variation = self.__random_obj.uniform(self.__variation_min, self.__variation_max)
        pm = self.__base_value + variation
        # add the variance percentage based on the season
        return pm + pm * self._get_seasonal_variation(self) / 100


    def simulate(self) -> str:
        timestamp = self._datetime_obj.now()
        self.__value = self._generate_air_pollution()

        reading = {
            "type": "%",
            "value": round(self.__value, 2)
        }

        dato = json_message_maker(SensorTypes.AIR_POLLUTION, str(timestamp), [reading], self._sensor_name, self._coordinates)

        return dato
