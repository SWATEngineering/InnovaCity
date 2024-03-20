from src.utils.sensor_types import SensorTypes
from src.utils.coordinates import Coordinates

from typing import List, Dict
import json


def json_message_maker(sensor_type: SensorTypes, timestamp: str, readings: List[Dict], name: str, location: Coordinates):
    return json.dumps({
        "type": sensor_type.value,
        "timestamp": timestamp,
        "readings": readings,
        "name": name,
        "location": json.loads(location.get_geo_json())
    })
