from src.utils.sensor_types import SensorTypes

from src.simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from src.simulator.wind_sensor_simulator import WindSensorSensorSimulator
from src.simulator.rain_sensor_simulator import RainSensorSensorSimulator
from src.simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from src.simulator.air_pollution_simulator import AirPollutionSensorSimulator
from src.simulator.reservoir_sensor_simulator import ReservoirSensorSimulator

str_to_type_switcher = {
    SensorTypes.TEMPERATURE.value: (SensorTypes.TEMPERATURE, TemperatureSensorSensorSimulator),
    SensorTypes.HUMIDITY.value: (SensorTypes.HUMIDITY, HumiditySensorSensorSimulator),
    SensorTypes.WIND.value: (SensorTypes.WIND, WindSensorSensorSimulator),
    SensorTypes.RAIN.value: (SensorTypes.RAIN, RainSensorSensorSimulator),
    SensorTypes.RESERVOIR.value: (SensorTypes.RESERVOIR, ReservoirSensorSimulator),
    SensorTypes.AIR_POLLUTION.value: (SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator),
    SensorTypes.PARKING.value: (SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator),
    SensorTypes.CHARGING_STATION.value: (SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator),
    SensorTypes.ECO_ZONE.value: (SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator),
    SensorTypes.TRAFFIC.value: (SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator),
    SensorTypes.ELECTRIC_BICYCLE.value: (SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator)
}
