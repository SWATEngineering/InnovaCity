from src.utils.sensor_types import SensorTypes
from src.utils.coordinates import Coordinates

from typing import List, Dict
import json


def json_message_maker(type: SensorTypes, timestamp: str, readings: List[Dict], name: str, location: Coordinates):
    return json.dumps({
        "type": type.value,
        "timestamp": timestamp,
        "readings": readings,
        "name": name,
        "location": json.loads(location.get_geo_json())
    })
