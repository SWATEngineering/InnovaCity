from random import Random
from typing import Dict, Type
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

    def __init__(self, configs: str):
        super().__init__(configs)

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
            ), self.__writer
        ))
