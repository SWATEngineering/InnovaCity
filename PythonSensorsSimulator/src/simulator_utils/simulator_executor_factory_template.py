from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Type
import json

from simulator_utils.simulator_executor import SimulatorExecutor

from utils.sensor_types import SensorTypes

from simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from simulator.wind_sensor_simulator import WindSensorSensorSimulator
from simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from simulator.rain_sensor_simulator import RainSensorSensorSimulator
from simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from simulator.air_pollution_simulator import AirPollutionSensorSimulator
from simulator.reservoir_sensor_simulator import ReservoirSensorSimulator


class SimulatorExecutorFactoryTemplate(ABC, BaseModel):
    @abstractmethod
    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
        pass

    def create(self) -> SimulatorExecutor:
        sensors_config = json.loads(self.__configs)
        for sensor_config in sensors_config:
            if sensor_config['type'] == SensorTypes.TEMPERATURE.value:
                self.__create_simulator(sensor_config, SensorTypes.TEMPERATURE, TemperatureSensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.RAIN.value:
                self.__create_simulator(sensor_config, SensorTypes.RAIN, RainSensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.RESERVOIR.value:
                self.__create_simulator(sensor_config, SensorTypes.RESERVOIR, ReservoirSensorSimulator)
            elif sensor_config['type'] == SensorTypes.WIND.value:
                self.__create_simulator(sensor_config, SensorTypes.WIND, WindSensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.AIR_POLLUTION.value:
                self.__create_simulator(sensor_config, SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator)
            elif sensor_config['type'] == SensorTypes.HUMIDITY.value:
                self.__create_simulator(sensor_config, SensorTypes.HUMIDITY, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.HYDROLOGICAL.value:
                self.__create_simulator(sensor_config, SensorTypes.HYDROLOGICAL, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.CHARGING_STATION.value:
                self.__create_simulator(sensor_config, SensorTypes.CHARGING_STATION, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.ECO_ZONE.value:
                self.__create_simulator(sensor_config, SensorTypes.ECO_ZONE, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.ELECTRIC_BICYCLE.value:
                self.__create_simulator(sensor_config, SensorTypes.ELECTRIC_BICYCLE, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.PARKING.value:
                self.__create_simulator(sensor_config, SensorTypes.PARKING, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.TRAFFIC.value:
                self.__create_simulator(sensor_config, SensorTypes.TRAFFIC, HumiditySensorSensorSimulator)
            return SimulatorExecutor(_SimulatorExecutor__simulators=self.__simulators)
