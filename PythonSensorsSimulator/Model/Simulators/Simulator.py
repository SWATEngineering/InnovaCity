from abc import ABC, abstractmethod

from ..Writers import Writer


class Simulator(ABC):
    __writer: Writer = None
    __frequency_in_s: int = None
    __continue_simulating: bool = None
    __id = None

    def __init__(self, writer: Writer, id: str, frequency_in_s: int = 1):
        self.__writer = writer
        self.__frequency_in_s = frequency_in_s
        self.__continue_simulating = True
        self.__id = id

    @abstractmethod
    def simulate(self) -> None:
        pass

    def stop_simulating(self) -> None:
        self.__continue_simulating = False
