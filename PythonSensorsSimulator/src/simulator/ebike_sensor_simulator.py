from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from math import radians, sin, cos, sqrt
import json
import time
from datetime import datetime
from src.utils.coordinates import Coordinates
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker

class EBikeSensorSimulator(SensorSimulatorStrategy):
    __bike_percentage: float = 100
    __last_coordinates: Coordinates = None
    __last_timestamp: datetime = None
    __is_charging: bool = False

    def __init__(self, **data):
        super().__init__(**data)

    def _charge_battery(self) -> None:
        if self.__is_charging == False:
            self.__is_charging = True

        increment = self._random_obj.uniform(1, 2)
        self.__bike_percentage += increment

        if self.__bike_percentage >= 99.99:
            self.__is_charging = False

    def _calculate_movement(self) -> None:
        last_lon, last_lat = json.loads(self.__last_coordinates.get_geo_json())['coordinates']

        new_lat = last_lat + self._random_obj.uniform(-0.001, 0.001)
        new_lon = last_lon + self._random_obj.uniform(-0.001, 0.001)

        self._coordinates = Coordinates(latitude=new_lat, longitude=new_lon)

    def _calculate_distance(self) -> float:
        lat1, lon1 = json.loads(self._coordinates.get_geo_json())['coordinates']
        lat2, lon2 = json.loads(self.__last_coordinates.get_geo_json())['coordinates']
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        distance = sqrt(dlat ** 2 + dlon ** 2)

        return distance

    def _measure_battery_level(self) -> float:
        if self.__last_coordinates is None or self.__last_timestamp is None:
            return self.__bike_percentage
        
        if self.__bike_percentage <= 0.01 or self.__is_charging == True:
            self._charge_battery()
        if self.__is_charging == True:
            return self.__bike_percentage

        self._calculate_movement()

        l_lon, l_lat = json.loads(self.__last_coordinates.get_geo_json())['coordinates']
        n_lon, n_lat = json.loads(self._coordinates.get_geo_json())['coordinates']
        if l_lon == n_lon and l_lat == n_lat:
            return self.__bike_percentage
        
        time_difference = (self._datetime_obj.datetime.now() - self.__last_timestamp).total_seconds()
        distance = self._calculate_distance()

        speed = distance / time_difference
        battery_drainage = speed * 0.1
        percentage = self.__bike_percentage - battery_drainage

        percentage = max(0.0, min(100.0, percentage))

        return percentage

    def simulate(self) -> str:
        self.__bike_percentage = self._measure_battery_level()

        reading = {
            "type": "%",
            "value": round(self.__bike_percentage, 2)
        }

        self.__last_coordinates = self._coordinates
        self.__last_timestamp = self._datetime_obj.datetime.now()

        dato = json_message_maker(SensorTypes.ELECTRIC_BICYCLE, str(self.__last_timestamp), [reading], self._sensor_name, self._coordinates)

        return dato