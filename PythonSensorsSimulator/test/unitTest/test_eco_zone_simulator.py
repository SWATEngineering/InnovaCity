import json
from datetime import datetime,timedelta
from unittest.mock import patch
from src.simulator.ecozone_sensor_simulator import EcoZoneSensorSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random

def test_eco_zone_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining specific values for randint and uniform
    tasso_massimo = 0.2
    svuotamento = 22
    inizio = 3

    # Defining a specific datetime for the simulation (daytime)
    simulated_datetime_day = datetime(2024, 3, 18, 10, 30, 20, 447663)
    # Defining a specific datetime for the simulation (nighttime)
    simulated_datetime_night = datetime(2024, 3, 18, 2, 0, 0, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform') as mock_uniform:
        # Settiamo i valori che si desidera che uniform restituisca
        mock_uniform.side_effect = [0.5, 0.25, 0.0]  # Valori diversi per il giorno e la notte

        with patch.object(Random, 'random', return_value=0):
            random_obj = Random(123)

            # Mocking randint with specific values
            with patch('random.randint', side_effect=[tasso_massimo, svuotamento, inizio]):
                # Mocking datetime object to return the specific datetime for daytime
                with patch('datetime.datetime') as mocked_datetime:
                    # Usiamo il datetime diurno
                    mocked_datetime.now.return_value = simulated_datetime_day

                    # Creating an instance of the EcoZoneSensorSensorSimulator with coordinates
                    sensor_simulator = EcoZoneSensorSensorSimulator("eco_zone1", random_obj, mocked_datetime,
                                                                      coordinates)

                    # Running the simulate method to get the JSON data
                    json_data_day = sensor_simulator.simulate()

                    # Parsing the JSON data
                    parsed_json_day = json.loads(json_data_day)

                    # Define the expected JSON structure for daytime
                    expected_json_day = {
                        "type": "eco_zone",
                        "timestamp": "2024-03-18 10:30:20.447663",
                        "readings": [{"type": "%", "value": 44.13}],
                        "name": "eco_zone1",
                        "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                    }

                    # Assert that the parsed JSON for daytime matches the expected JSON
                    assert parsed_json_day == expected_json_day


def test_eco_zone_sensor_simulation_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Defining the range for temperature
    min = -1
    max = 100

    # Running the simulation 1000 times with different timestamps
    for i in range(24*60):
        # Creating a timestamp for the simulation
        simulated_datetime = datetime(2024, 3, 18, 0, 0, 0) + timedelta(minutes=i)
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            # Creating an instance of the TemperatureSensorSensorSimulator with coordinates
            sensor_simulator = EcoZoneSensorSensorSimulator("eco_zone1", random_obj, mocked_datetime,
                                                                coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Extracting the temperature value
            percentuale = parsed_json['readings'][0]['value']

            # Assert that the temperature is within the specified range
            assert min <= percentuale <= max




