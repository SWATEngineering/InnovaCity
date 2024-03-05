from abc import ABC, abstractmethod
from typing import Callable


class TargetProducer(ABC):

    @abstractmethod
    def produce(self, message: str, callback: Callable) -> None:
        pass
