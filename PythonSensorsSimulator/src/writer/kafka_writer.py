from writer_strategy import WriterStrategy
from pydantic import BaseModel
from kafka_logic.adapter_producer import AdapterProducer
from utils.utility_functions import acked


class KafkaWriter(WriterStrategy, BaseModel):
    __producer: AdapterProducer

    def write(self, to_write: str) -> None:
        self.__producer.produce(to_write, acked)
