import uuid

from abc import ABC, abstractmethod
from ..Writers import Writer


class Simulator(ABC):
    __writer: Writer = None
    __frequency_in_s: int = None
    __continue_simulating: bool = None
    __uuid: uuid = None

    def __init__(self, writer: Writer, frequency_in_s: int = 1):
        self.__writer = writer
        self.__frequency_in_s = frequency_in_s
        self.__continue_simulating = True
        self.__uuid = uuid.uuid4()

    @abstractmethod
    def simulate(self) -> None:
        pass

    def stop_simulating(self) -> None:
        self.__continue_simulating = False

    def continue_simulating(self) -> bool:
        return self.__continue_simulating

    def get_uuid(self) -> uuid:
        return self.__uuid

    def get_writer(self) -> Writer:
        return self.__writer

    def get_frequency_is_s(self):
        return self.__frequency_in_s
