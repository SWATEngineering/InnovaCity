from random import Random
from typing import Dict, Type
from datetime import datetime
from .simulator_thread import SimulatorThread
from .simulator_executor_factory_template import SimulatorExecutorFactoryTemplate

from src.utils.sensor_types import SensorTypes
from src.utils.coordinates import Coordinates

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.writer.kafka_writer import KafkaWriter
from src.writer.kafka_logic.adapter_producer import AdapterProducer


class KafkaSimulatorExecutorFactory(SimulatorExecutorFactoryTemplate):
    __data_broker_host: str = 'kafka'
    __data_broker_port: int = 9092
    __writers: Dict[str, KafkaWriter] = {}
    __simulators_counter: Dict[str, int] = {}

    def __init__(self, configs: str, data_broker_host: str, data_broker_port: int):
        super().__init__(configs)
        self.__data_broker_host = data_broker_host
        self.__data_broker_port = data_broker_port

    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
        sensor_name = simulator_type.value
        if "name" in config:
            if "name" in self.__simulators_counter:
                raise Exception("Non si può impostare lo stesso nome su due sensori diversi.")
            sensor_name = config["name"]
            self.__simulators_counter[sensor_name] = 1
        else:
            self.__simulators_counter[simulator_type.value] = self.__simulators_counter.get(simulator_type.value, 0) + 1
            sensor_name += str(self.__simulators_counter[simulator_type.value])
        if simulator_type.value not in self.__writers:
            self.__writers[simulator_type.value] = KafkaWriter(
                producer=AdapterProducer(
                    simulator_type, self.__data_broker_host, self.__data_broker_port
                )
            )
        self._simulators.append(SimulatorThread(
            config["wait_time_in_seconds"],
            cls(
                sensor_name=sensor_name,
                random_obj=Random(),
                datetime_obj=datetime,
                coordinates=Coordinates(
                    longitude=config["location"]["coordinates"][0],
                    latitude=config["location"]["coordinates"][1]
                )
            ), self.__writers[simulator_type.value]
        ))
