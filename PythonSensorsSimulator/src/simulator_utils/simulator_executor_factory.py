from io import FileIO
from pydantic import BaseModel
from simulator_executor import SimulatorExecutor
from utils.sensor_types import SensorTypes
from simulator_thread import SimulatorThread
from simulator.temperature_sensor_simulator import TemperatureSensorSensorSimulator
from simulator.wind_sensor_simulator import WindSensorSensorSimulator
from simulator.rain_sensor_simulator import RainSensorSensorSimulator
from simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from simulator.air_pollution_simulator import AirPollutionSensorSimulator
from writer.kafka_writer import KafkaWriter
from writer.kafka_logic.adapter_producer import AdapterProducer
import json

class SimulatorExecutorFactory(BaseModel):
    __config_file_name: str = 'simulator_config.json'
    __data_broker_host: str = 'kafka'
    __data_broker_port: int = 9092
    __io_module: FileIO

    def __init__(self, /, broker_host: str = "kafka", broker_port: int = 9092,
                 config_file_name: str = 'simulators_config.json'):
        self.__config_file_name = config_file_name
        self.__data_broker_host = broker_host
        self.__data_broker_port = broker_port
        self.__io_module = FileIO(config_file_name, mode="r")

# TODO: serve un factory anche per i simulatori
    def create(self) -> SimulatorExecutor:

        simulators = []
        writers = {}
        sensors_config = {}
        with self.__io_module:
            sensors_config = json.loads(self.__io_module.read())
        for sensor_config in sensors_config:
            if sensor_config['type'] == SensorTypes.TEMPERATURE.value:
                if writers[SensorTypes.TEMPERATURE.value] is None:
                    writers[SensorTypes.TEMPERATURE.value] = KafkaWriter(
                        _KafkaWriter__producer=AdapterProducer(
                            SensorTypes.TEMPERATURE.value,
                            self.__data_broker_host,self.__data_broker_port)
                    )
                simulators.append(SimulatorThread(TemperatureSensorSensorSimulator()))
            elif sensor_config['type'] == SensorTypes.RAIN.value:
                pass
            elif sensor_config['type'] == SensorTypes.WIND.value:
                pass
            elif sensor_config['type'] == SensorTypes.AIR_POLLUTION.value:
                pass
            elif sensor_config['type'] == SensorTypes.HUMIDITY.value:
                pass
            # elif sensor_config['type'] == SensorTypes.HYDROLOGICAL.value:
            # elif sensor_config['type'] == SensorTypes.CHARGING_STATION.value:
            # elif sensor_config['type'] == SensorTypes.ECO_ZONE.value:
            # elif sensor_config['type'] == SensorTypes.ELECTRIC_BICYCLE.value:
            # elif sensor_config['type'] == SensorTypes.PARKING.value:
            # elif sensor_config['type'] == SensorTypes.TRAFFIC.value:
