from random import Random
from typing import List, Dict, Type
import datetime
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

    def __init__(self, **data):
        super().__init__(**data)

    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
        if self.__writers[simulator_type.value] is None:
            self.__writers[simulator_type.value] = KafkaWriter(
                _KafkaWriter__producer=AdapterProducer(
                    simulator_type.value, self.__data_broker_host, self.__data_broker_port
                )
            )
        self.__simulators_counter[simulator_type.value] = self.__simulators_counter.get(simulator_type.value, 0) + 1
        self._simulators.append(SimulatorThread(
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
