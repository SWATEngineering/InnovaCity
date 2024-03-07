from src.writer.writer_strategy import WriterStrategy
from src.writer.kafka_logic.target_producer import TargetProducer
from src.utils.utility_functions import acked

from pydantic import BaseModel


class KafkaWriter(WriterStrategy, BaseModel):
    __producer: TargetProducer

    def write(self, to_write: str) -> None:
        self.__producer.produce(to_write, acked)
