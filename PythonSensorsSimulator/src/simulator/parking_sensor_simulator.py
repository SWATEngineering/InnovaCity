import numpy as np
from datetime import datetime
from random import Random
from src.utils.coordinates import Coordinates
from typing import Type
from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.json_message_maker import json_message_maker
from src.utils.sensor_types import SensorTypes
from dataclasses import dataclass


@dataclass
class ParkingGaussianPeak:
    mean_position_in_minutes: int
    std_dev_in_minutes: int
    weight: float


class ParkingSensorSimulator(SensorSimulatorStrategy):
    __peak1: ParkingGaussianPeak
    __peak2: ParkingGaussianPeak
    __max_cars: int
    __total_minutes_in_day: int
    __noise_scale: float
    __daily_data: np.ndarray

    def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
        super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
        self.__peak1 = ParkingGaussianPeak(12 * 60, 120, 0.6)
        self.__peak2 = ParkingGaussianPeak(21 * 60, 30, 0.3)
        self.__max_cars = 100
        self.__total_minutes_in_day = 24 * 60
        self.__noise_scale = 0.03
        self.__daily_data = self.__generate_dual_peak_gaussian()


    def __generate_dual_peak_gaussian(self) -> np.ndarray:
        minutes = np.arange(self.__total_minutes_in_day)
        peak1_vals: list = (self.__peak1.weight *
                      np.exp(
                          -((minutes - self.__peak1.mean_position_in_minutes) / self.__peak1.std_dev_in_minutes) ** 2))
        peak2_vals: list = (self.__peak2.weight *
                      np.exp(
                          -((minutes - self.__peak2.mean_position_in_minutes) / self.__peak2.std_dev_in_minutes) ** 2))

        # Adding random noise to the peaks
        peak1_vals = [x + self._random_obj.normalvariate(0, 1) * self.__noise_scale for x in peak1_vals]
        peak1_vals = [0 if x < 0 else x for x in peak1_vals]  # Set negative values to 0
        peak2_vals = [x + self._random_obj.normalvariate(0, 1) * self.__noise_scale for x in peak2_vals]
        peak2_vals = [0 if x < 0 else x for x in peak2_vals]  # Set negative values to 0

        total_cars = peak1_vals + peak2_vals
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
            "value": round(self.__daily_data[minutes_from_midnight])
        }
        # Send how many parking lots it has
        reading2 = {
            "type": "Number",
            "value": self.__max_cars
        }

        dato = json_message_maker(SensorTypes.PARKING, str(now), [reading1, reading2], self._sensor_name,
                                  self._coordinates)

        return dato
