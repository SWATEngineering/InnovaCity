from random import Random
from typing import List, Dict, Type
import datetime

from simulator_thread import SimulatorThread
from simulator_executor_factory_template import SimulatorExecutorFactoryTemplate

from utils.sensor_types import SensorTypes
from utils.coordinates import Coordinates

from simulator.sensor_simulator_strategy import SensorSimulatorStrategy

from writer.std_out_writer import StdoutWriter


class StdoutSimulatorExecutorFactory(SimulatorExecutorFactoryTemplate):
    __configs: str
    __simulators: List[SimulatorThread] = []
    __simulators_counter: Dict[str, int] = {}
    __writer: StdoutWriter = StdoutWriter()

    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
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
            ), self.__writer
        ))

