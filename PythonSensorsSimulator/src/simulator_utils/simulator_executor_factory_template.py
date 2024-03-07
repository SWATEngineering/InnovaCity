from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Type, List
import json

from src.simulator_utils.simulator_executor import SimulatorExecutor
from src.simulator_utils.simulator_thread import SimulatorThread

from src.utils.sensor_types import SensorTypes

from src.simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from src.simulator.wind_sensor_simulator import WindSensorSensorSimulator
from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.simulator.rain_sensor_simulator import RainSensorSensorSimulator
from src.simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from src.simulator.air_pollution_simulator import AirPollutionSensorSimulator
from src.simulator.reservoir_sensor_simulator import ReservoirSensorSimulator


class SimulatorExecutorFactoryTemplate(ABC, BaseModel):
    _configs: str
    _simulators: List[SimulatorThread] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._configs = data.get('configs')

    @abstractmethod
    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
        pass

    def create(self) -> SimulatorExecutor:
        sensors_config = json.loads(self._configs)
        for sensor_config in sensors_config:
            if sensor_config['type'] == SensorTypes.TEMPERATURE.value:
                self._create_simulator(sensor_config, SensorTypes.TEMPERATURE, TemperatureSensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.RAIN.value:
                self._create_simulator(sensor_config, SensorTypes.RAIN, RainSensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.RESERVOIR.value:
                self._create_simulator(sensor_config, SensorTypes.RESERVOIR, ReservoirSensorSimulator)
            elif sensor_config['type'] == SensorTypes.WIND.value:
                self._create_simulator(sensor_config, SensorTypes.WIND, WindSensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.AIR_POLLUTION.value:
                self._create_simulator(sensor_config, SensorTypes.AIR_POLLUTION, AirPollutionSensorSimulator)
            elif sensor_config['type'] == SensorTypes.HUMIDITY.value:
                self._create_simulator(sensor_config, SensorTypes.HUMIDITY, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.CHARGING_STATION.value:
                self._create_simulator(sensor_config, SensorTypes.CHARGING_STATION, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.ECO_ZONE.value:
                self._create_simulator(sensor_config, SensorTypes.ECO_ZONE, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.ELECTRIC_BICYCLE.value:
                self._create_simulator(sensor_config, SensorTypes.ELECTRIC_BICYCLE, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.PARKING.value:
                self._create_simulator(sensor_config, SensorTypes.PARKING, HumiditySensorSensorSimulator)
            elif sensor_config['type'] == SensorTypes.TRAFFIC.value:
                self._create_simulator(sensor_config, SensorTypes.TRAFFIC, HumiditySensorSensorSimulator)
            return SimulatorExecutor(simulators=self._simulators)
