from abc import ABC, abstractmethod


class WriterStrategy(ABC):

    @abstractmethod
    def write(self, to_write: str) -> None:
        pass
