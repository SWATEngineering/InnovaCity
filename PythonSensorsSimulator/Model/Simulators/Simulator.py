from abc import ABC, abstractmethod

from ..Writers import Writer


class Simulator(ABC):
    writer: Writer = None
    frequency_in_s: int = None
    continue_simulating: bool = None
    id = None

    def __init__(self, writer: Writer, id: str, frequency_in_s: int = 1):
        self.writer = writer
        self.frequency_in_s = frequency_in_s
        self.continue_simulating = True
        self.id = id

    @abstractmethod
    def simulate(self) -> None:
        pass

    def stop_simulating(self) -> None:
        self.continue_simulating = False
