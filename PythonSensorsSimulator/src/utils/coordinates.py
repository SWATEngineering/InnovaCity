from pydantic import BaseModel
import json


class Coordinates(BaseModel):
    __longitude: float
    __latitude: float

    def __init__(self,**data):
        super().__init__(**data)
        self.__longitude = data['longitude']
        self.__latitude = data['latitude']

    def get_geo_json(self) -> str:
        return json.dumps({
            "type": "Point",
            "coordinates": [self.__longitude, self.__latitude]
        })
