from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
import matplotlib.pyplot as plt


class AirPollutionSensorSimulator(SensorSimulatorStrategy):
    __value: float  # value read by the sensor
    __base_value: float = 10
    __variation_min: float = -3
    __variation_max: float = 3
    __month: int

    def __init__(self, **data):
        super().__init__(**data)
        self.__month = self._datetime_obj.now().month

    # return the variation percentage based on the season
    def _get_seasonal_variation(self) -> float:

        if self.__month in [12, 1, 2]:  # winter
            # air pollution is higher due to the heating
            return 20  # % added
        elif self.__month in [3, 4, 5]:  # spring
            return 5  # %
        elif self.__month in [6, 7, 8]:  # summer
            return 0  # %
        elif self.__month in [9, 10, 11]:  # autumn
            return 5  # %
        else:
            print("Error: month not valid")
            exit(1)

    # generate air pollution value
    def _generate_air_pollution(self) -> float:

        # add the variance percentage based on the season
        value = self.__base_value + self.__base_value * self._get_seasonal_variation() / 100
        # add random variation
        variation = self._random_obj.uniform(self.__variation_min, self.__variation_max)

        return value + variation

    def simulate(self) -> str:
        timestamp = self._datetime_obj.now()
        self.__value = self._generate_air_pollution()

        reading = {
            "type": "%",
            "value": round(self.__value, 2)
        }

        dato = json_message_maker(SensorTypes.AIR_POLLUTION, str(timestamp), [reading], self._sensor_name,
                                  self._coordinates)

        return dato

    def simulate_and_plot(self, num_iterations=100):
        pollution_values = []

        for _ in range(num_iterations):
            value = self._generate_air_pollution()
            pollution_values.append(value)

        plt.plot(range(1, num_iterations + 1), pollution_values, marker='o')
        plt.xlabel('Iterations')
        plt.ylabel('Air Pollution Value')
        plt.title('Air Pollution Simulation Results')
        plt.grid(True)
        plt.show()