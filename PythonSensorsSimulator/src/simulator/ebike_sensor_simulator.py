from random import Random, choice, uniform
from typing import Type
import requests
import os

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from math import radians, sqrt
import json
from datetime import datetime
from src.utils.coordinates import Coordinates
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker


class EBikeSensorSimulator(SensorSimulatorStrategy):
    __bike_percentage: float = 100

    __last_coordinate_index: int = 0
    __source: tuple = ()
    __destination: tuple = ()
    __route_coordinates: list = []

    __last_timestamp: datetime = None
    __is_charging: bool = False

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self.__source = json.loads(self._coordinates.get_geo_json())['coordinates']
        self.__destination = self._pick_destination()
        self.__route_coordinates = self._get_route_coordinates()

    def _charge_battery(self) -> None:
        if not self.__is_charging:
            self.__is_charging = True

        increment = self._random_obj.uniform(1, 2)
        self.__bike_percentage += increment

        if self.__bike_percentage >= 99.99:
            self.__is_charging = False

    def _pick_destination(self) -> tuple:
        lat, lon = json.loads(self._coordinates.get_geo_json())['coordinates']
        API_KEY = os.environ.get("ORS_API_KEY")

        lat_range = 0.1
        lon_range = 0.1

        dest_latitude = uniform(lat - lat_range, lat + lat_range)
        dest_longitude = uniform(lon - lon_range, lon + lon_range)

        url = f"https://api.openrouteservice.org/geocode/reverse?api_key={API_KEY}&point.lon={dest_longitude}&point.lat={dest_latitude}"

        headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'}
        response = requests.get(url, headers=headers)
        #print("Calling API ...:", response.status_code, response.reason)

        data = response.json()
        coordinates = []
        for feature in data['features']:
            coordinates.append(feature['geometry']['coordinates'])

        new_destination = choice(coordinates)
        dest_longitude, dest_latitude = new_destination

        return (dest_latitude, dest_longitude)

    def _get_route_coordinates(self) -> list:
        source = self.__source
        dest = self.__destination
        start = "{},{}".format(source[1], source[0])
        end = "{},{}".format(dest[1], dest[0])
        API_KEY = os.environ.get("ORS_API_KEY")

        url = f"https://api.openrouteservice.org/v2/directions/cycling-electric?api_key={API_KEY}&start={start}&end={end}"

        headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',}
        call = requests.get(url, headers=headers)
        #print("Calling API ...:", call.status_code, call.reason)
        response_text = call.text

        routejson = json.loads(response_text)
        coordinates = []

        for coordinate in routejson['features'][0]['geometry']['coordinates']:
            coordinates.append((coordinate[0], coordinate[1]))

        return coordinates

    def _calculate_movement(self) -> None:
        if self.__last_coordinate_index == len(self.__route_coordinates) - 1:
            self.__source = self.__destination
            self._pick_destination()
            self._get_route_coordinates()
            self.__last_coordinate_index = 0
        next_coordinate_index = self.__last_coordinate_index + 1
        next_coordinate = self.__route_coordinates[next_coordinate_index]

        self._coordinates = Coordinates(latitude=next_coordinate[0], longitude=next_coordinate[1])

    def _calculate_distance(self) -> float:
        lat1, lon1 = json.loads(self._coordinates.get_geo_json())['coordinates']
        lat2, lon2 = self.__route_coordinates[self.__last_coordinate_index]
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        distance = sqrt(dlat ** 2 + dlon ** 2)

        return distance

    def _measure_battery_level(self) -> float:
        if self.__last_timestamp is None:
            return self.__bike_percentage

        if self.__bike_percentage <= 0.01 or self.__is_charging == True:
            self._charge_battery()
        if self.__is_charging:
            return self.__bike_percentage

        self._calculate_movement()

        time_difference = (self._datetime_obj.now() - self.__last_timestamp).total_seconds()
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

        if not self.__last_timestamp is None and not self.__is_charging:
            self.__last_coordinate_index += 1
        self.__last_timestamp = self._datetime_obj.now()

        dato = json_message_maker(SensorTypes.ELECTRIC_BICYCLE, str(self.__last_timestamp), [reading],
                                  self._sensor_name, self._coordinates)

        return dato
