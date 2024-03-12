from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
from src.utils.sensor_types import SensorTypes
from src.utils.json_message_maker import json_message_maker
import datetime


class ChargingStationSimulator(SensorSimulatorStrategy):

    def __init__(self, **data):
        super().__init__(**data)
        self.__in_use = False
        self.__time_to_complete_charge = None
        self.__next_connection = self._datetime_obj.now() + \
            datetime.timedelta(
                seconds=self._random_obj.randint(1800, 7000))

    def __connect_car(self):
        self.__in_use = True

        self.__mean_erogation_power = self._random_obj.uniform(20, 80)
        # sono più o meno i tempi per la ricarica di con un erogazione di 50 wat
        # quindi 2 è il tempo di ricarica per avere il 100%
        random_duration = self._random_obj.randint(int(0.5 * 3600), 2 * 3600)
        self.__time_to_complete_charge = self._datetime_obj.now() + \
            datetime.timedelta(seconds=random_duration)

    def __check_new_car(self):
        if self.__next_connection is None or self._datetime_obj.now() >= self.__next_connection:
            self.__connect_car()

    def __remove_car_from_charging(self):
        # l'auto viene rimossa dalla carica solo se al 100%
        if self._datetime_obj.now() >= self.__time_to_complete_charge:
            disconnect_probability = 1 / 1800
            random_number = self._random_obj.random()
            if random_number < disconnect_probability:
                self.__in_use = False
                self.__next_connection = self._datetime_obj.now() + \
                    datetime.timedelta(
                        seconds=self._random_obj.randint(1800, 7000))

    def __get_erogation(self) -> int:
        if not self.__in_use:
            return 0  # No charging if the column is not in use
        if self._datetime_obj.now() < self.__time_to_complete_charge:
            # voglio che più tempo manca alla carica più forte è l'erogazione

            current_time = self._datetime_obj.now().time()
            completion_time = self.__time_to_complete_charge.time()
            # il tempo mancante alla fine della carica
            time_difference_seconds = (current_time.hour * 3600 + current_time.minute * 60 + current_time.second) - \
                (completion_time.hour * 3600 +
                 completion_time.minute * 60 + completion_time.second)

            erogation = self.__mean_erogation_power + \
                self._random_obj.uniform(-0.05, 0.05) - \
                (self.__mean_erogation_power * 0.1) * \
                time_difference_seconds / (2*3600)
            # cosi ad intuito dovrebbe funzionare come si deve
        else:
            erogation = 0.1 + self._random_obj.uniform(-0.05, 0.05)
        return erogation

    def simulate(self) -> int:
        if not self.__in_use:
            self.__check_new_car()
        else:
            self.__remove_car_from_charging()

        state = self.__in_use
        erogation = self.__get_erogation()

        return json_message_maker(SensorTypes.CHARGING_STATION, str(self._datetime_obj.now()), [
            {
                "type": "kW/h",
                "value": "{0:.2f}".format(erogation)
            },
            {
                "type": "availability",
                "value": state
            }
        ], self._sensor_name, self._coordinates)
