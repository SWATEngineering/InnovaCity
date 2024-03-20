import numpy as np
from datetime import datetime
from random import Random
from src.utils.coordinates import Coordinates
from typing import Type
from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.json_message_maker import json_message_maker
from src.utils.sensor_types import SensorTypes


class ParkingSensorSimulator(SensorSimulatorStrategy):
    __max_cars: int
    __peak1_mean_minutes: int
    __peak1_weight: float
    __peak1_std_dev_minutes: int
    __peak2_mean_minutes: int
    __peak2_weight: float
    __peak2_std_dev_minutes: int
    __total_minutes_in_day: int
    __noise_scale: float
    __daily_data: np.ndarray

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self.__max_cars = 100
        self.__peak1_mean_minutes = 12 * 60
        self.__peak1_weight = 0.6
        self.__peak1_std_dev_minutes = 120
        self.__peak2_mean_minutes = 21 * 60
        self.__peak2_weight = 0.3
        self.__peak2_std_dev_minutes = 30
        self.__total_minutes_in_day = 24 * 60
        self.__noise_scale = 0.01
        self.__daily_data = self.__generate_dual_peak_gaussian()

    def __generate_dual_peak_gaussian(self) -> np.ndarray:
        minutes = np.arange(self.__total_minutes_in_day)
        peak1 = (self.__peak1_weight *
                 np.exp(-((minutes - self.__peak1_mean_minutes) / self.__peak1_std_dev_minutes) ** 2))
        peak2 = (self.__peak2_weight *
                 np.exp(-((minutes - self.__peak2_mean_minutes) / self.__peak2_std_dev_minutes) ** 2))

        # Adding random noise to the peaks
        peak1 += self.__noise_scale * \
            np.random.normal(0, 1, self.__total_minutes_in_day)
        peak1[peak1 < 0] = 0  # Set negative values to 0
        peak2 += self.__noise_scale * \
            np.random.normal(0, 1, self.__total_minutes_in_day)
        peak2[peak2 < 0] = 0  # Set negative values to 0

        total_cars = peak1 + peak2
        scaled_cars = total_cars / np.max(total_cars) * self.__max_cars
        return scaled_cars

    @staticmethod
    def __minutes_from_midnight(now) -> int:
        """
        Calculate the number of minutes that have passed since midnight.

        Returns:
        int: Number of minutes.
        """
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = now - midnight
        minutes = delta.total_seconds() / 60
        return int(minutes)

    def simulate(self) -> str:
        now = self._datetime_obj.now()
        minutes_from_midnight = self.__minutes_from_midnight(now)
        if minutes_from_midnight == 0:
            self.__daily_data = self.__generate_dual_peak_gaussian()

        # Send how many cars are there in the parking
        reading1 = {
            "type": "Number",
            "value": self.__daily_data[minutes_from_midnight]
        }
        # Send how many parking lots it has
        reading2 = {
            "type": "Number",
            "value": self.__max_cars
        }

        dato = json_message_maker(SensorTypes.PARKING, str(now), [reading1, reading2], self._sensor_name,
                                  self._coordinates)

        return dato
