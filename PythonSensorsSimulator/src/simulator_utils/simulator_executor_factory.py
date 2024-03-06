from random import Random
from typing import List, Dict, Type
import datetime
import json

from pydantic import BaseModel

from simulator_executor import SimulatorExecutor
from simulator_thread import SimulatorThread

from utils.sensor_types import SensorTypes
from utils.coordinates import Coordinates

from simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from simulator.wind_sensor_simulator import WindSensorSensorSimulator
from simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from simulator.rain_sensor_simulator import RainSensorSensorSimulator
from simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from simulator.air_pollution_simulator import AirPollutionSensorSimulator
from simulator.reservoir_sensor_simulator import ReservoirSensorSimulator

from writer.kafka_writer import KafkaWriter
from writer.kafka_logic.adapter_producer import AdapterProducer


class SimulatorExecutorFactory(BaseModel):
    __configs: str
    __data_broker_host: str = 'kafka'
    __data_broker_port: int = 9092
    __simulators: List[SimulatorThread] = []
    __writers: Dict[str, KafkaWriter] = {}
    __simulators_counter: Dict[str, int] = {}

    def __create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
        if self.__writers[simulator_type.value] is None:
            self.__writers[simulator_type.value] = KafkaWriter(
                _KafkaWriter__producer=AdapterProducer(
                    simulator_type.value, self.__data_broker_host, self.__data_broker_port
                )
            )
        self.__simulators_counter[simulator_type.value] += self.__simulators_counter.get(simulator_type.value, 0) + 1
        self.__simulators.append(SimulatorThread(
            cls(
                _SensorSimulatorStrategy_wait_time_in_seconds=config["wait_time_in_seconds"],
                _SensorSimulatorStrategy_sensor_name=simulator_type.value + str(
                    self.__simulators_counter[simulator_type.value]
                ),
                _SensorSimulatorStrategy_random_obj=Random(),
                _SensorSimulatorStrategy_datetime_obj=datetime,
                _SensorSimulatorStrategy_coordinates=Coordinates(
                    __longitude=config["location"]["coordinates"][0],
                    __latitude=config["location"]["coordinates"][1]
                )
            ), self.__writers[simulator_type.value]
        ))

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
