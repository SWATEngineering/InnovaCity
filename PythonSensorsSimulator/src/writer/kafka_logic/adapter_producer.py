from typing import Callable

from confluent_kafka import Producer, KafkaException
from target_producer import TargetProducer
from utils.sensor_types import SensorTypes


class AdapterProducer(TargetProducer):
    __adaptee: Producer
    __topic: SensorTypes

    def __init__(self, topic: SensorTypes, ip: str, port: int):
        config = {'bootstrap.servers': ip + ':' + str(port)}
        self.__topic = topic
        try:
            self.__producer = Producer(config)
        except KafkaException as e:
            print(f"Errore nella creazione del producer: {e}")

    def produce(self, message: str, callback: Callable) -> None:
        self.__producer.produce(self.__topic.value, value=message, callback=callback)
        self.__producer.poll(1)
