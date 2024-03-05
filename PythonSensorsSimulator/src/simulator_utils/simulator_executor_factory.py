from io import FileIO
from pydantic import BaseModel
from simulator_executor import SimulatorExecutor


class SimulatorExecutorFactory(BaseModel):
    __config_file_name: str = 'simulator_config.json'
    __data_broker_host: str = 'kafka'
    __data_broker_port: int = 9092
    __io_module: FileIO

    def __init__(self, /, broker_host: str = "kafka", broker_port: int = 9092,
                 config_file_name: str = 'simulator_config.json'):
        self.__config_file_name = config_file_name
        self.__data_broker_host = broker_host
        self.__data_broker_port = broker_port
        self.__io_module = FileIO(config_file_name, mode="r")

    def create(self) -> SimulatorExecutor:
        pass
        #config = {}
        #with self.__io_module:

