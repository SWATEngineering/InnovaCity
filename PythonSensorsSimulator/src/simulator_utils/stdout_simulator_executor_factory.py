from random import Random
from typing import List, Dict, Type
from datetime import datetime

from src.simulator_utils.simulator_thread import SimulatorThread
from src.simulator_utils.simulator_executor_factory_template import SimulatorExecutorFactoryTemplate

from src.utils.sensor_types import SensorTypes
from src.utils.coordinates import Coordinates

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy

from src.writer.std_out_writer import StdoutWriter


class StdoutSimulatorExecutorFactory(SimulatorExecutorFactoryTemplate):
    __simulators_counter: Dict[str, int] = {}
    __writer: StdoutWriter = StdoutWriter()

    def __init__(self, **data):
        super().__init__(**data)

    def _create_simulator(self, config: Dict, simulator_type: SensorTypes, cls: Type[SensorSimulatorStrategy]):
        self.__simulators_counter[simulator_type.value] = self.__simulators_counter.get(simulator_type.value, 0) + 1
        self._simulators.append(SimulatorThread(
            config["wait_time_in_seconds"],
            cls(
                sensor_name=simulator_type.value + str(
                    self.__simulators_counter[simulator_type.value]
                ),
                random_obj=Random(),
                datetime_obj=datetime,
                coordinates=Coordinates(
                    longitude=config["location"]["coordinates"][0],
                    latitude=config["location"]["coordinates"][1]
                )
            ), self.__writer
        ))
