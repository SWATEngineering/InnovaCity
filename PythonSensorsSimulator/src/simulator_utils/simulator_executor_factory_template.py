from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Type, List
import json

from src.simulator_utils.simulator_executor import SimulatorExecutor
from src.simulator_utils.simulator_thread import SimulatorThread

from src.utils.sensor_types import SensorTypes

from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy

from src.utils.str_to_type_switcher import str_to_type_switcher


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
            type_tuple = str_to_type_switcher.get(sensor_config['type'], None)
            if type_tuple is not None:
                self._create_simulator(sensor_config, type_tuple[0], type_tuple[1])
        return SimulatorExecutor(simulators=self._simulators)
