from writer_strategy import WriterStrategy
from pydantic import BaseModel
from kafka_logic.target_producer import TargetProducer
from utils.utility_functions import acked


class KafkaWriter(WriterStrategy, BaseModel):
    __producer: TargetProducer

    def write(self, to_write: str) -> None:
        self.__producer.produce(to_write, acked)
