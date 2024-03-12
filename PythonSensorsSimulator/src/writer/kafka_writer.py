from src.writer.writer_strategy import WriterStrategy
from src.writer.kafka_logic.target_producer import TargetProducer
from src.utils.utility_functions import acked


class KafkaWriter(WriterStrategy):
    __producer: TargetProducer

    def __init__(self, producer: TargetProducer):
        self.__producer = producer

    def write(self, to_write: str) -> None:
        self.__producer.produce(to_write, acked)
