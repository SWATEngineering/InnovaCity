from enum import Enum


class SensorTypes(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WIND = "wind"
    RAIN = "rain"
    RESERVOIR = "reservoir"
    AIR_POLLUTION = "air_pollution"
    PARKING = "parking"
    CHARGING_STATION = "charging_station"
    ECO_ZONE = "eco_zone"
    TRAFFIC = "traffic"
    ELECTRIC_BICYCLE = "electric_bicycle"


