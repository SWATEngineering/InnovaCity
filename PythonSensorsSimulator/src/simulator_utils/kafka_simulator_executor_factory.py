from random import Random
from typing import List, Dict, Type
import datetime
import json

from pydantic import BaseModel

from simulator_executor import SimulatorExecutor
from simulator_thread import SimulatorThread
from simulator_executor_factory_template import SimulatorExecutorFactoryTemplate

from utils.sensor_types import SensorTypes
from utils.coordinates import Coordinates

from simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from simulator.wind_sensor_simulator import WindSensorSensorSimulator
from simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from simulator.rain_sensor_simulator import RainSensorSensorSimulator
from simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from simulator.air_pollution_simulator import AirPollutionSensorSimulator

from writer.kafka_writer import KafkaWriter
from writer.kafka_logic.adapter_producer import AdapterProducer


class KafkaSimulatorExecutorFactory(SimulatorExecutorFactoryTemplate):
    __configs: str
    __data_broker_host: str = 'kafka'
    __data_broker_port: int = 9092
    __simulators: List[SimulatorThread] = []
    __writers: Dict[str, KafkaWriter] = {}
    __simulators_counter: Dict[str, int] = {}

    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
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
