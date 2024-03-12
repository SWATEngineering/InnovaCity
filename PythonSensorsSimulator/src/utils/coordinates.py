import json


class Coordinates:
    __longitude: float
    __latitude: float

    def __init__(self, longitude: float, latitude: float):
        self.__longitude = longitude
        self.__latitude = latitude

    def get_geo_json(self) -> str:
        return json.dumps({
            "type": "Point",
            "coordinates": [self.__longitude, self.__latitude]
        })
