import json
from datetime import datetime, timedelta
from unittest.mock import patch
from src.simulator.rain_sensor_simulator import RainSensorSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random


def test_rain_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    simulated_datetime = datetime(2024, 3, 18, 10, 19, 9, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', return_value=0):
        with patch.object(Random, 'randint', side_effect=[1, 7200, 0]):
            random_obj = Random(123)

            # Mocking datetime object to return the specific datetime
            with patch('datetime.datetime') as mocked_datetime:
                mocked_datetime.now.return_value = simulated_datetime

                # Creating an instance of the RainSensorSimulator with coordinates
                simulator = RainSensorSensorSimulator(
                    "rain_sensor1", random_obj, mocked_datetime, coordinates)

                # Running the simulate method to get the JSON data
                json_data = simulator.simulate()

                # Parsing the JSON data
                parsed_json = json.loads(json_data)

                # Define the expected JSON structure
                expected_json = {
                    "type": "rain",
                    "timestamp": "2024-03-18 10:19:09.447663",
                    "readings": [
                        # Update expected value to string
                        {"type": "mm/mc", "value": 0.0}
                    ],
                    "name": "rain_sensor1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }

                # Assert that the parsed JSON matches the expected JSON
                assert parsed_json == expected_json


def test_rain_sensor_simulation_intensity_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)
    # Mocking random object
    random_obj = Random(123)  # set the seed to make the test reproducible
    datetime_obj = datetime(2024, 3, 18, 0, 0, 0) - timedelta(minutes=1)

    # Defining the range for rain intensity
    min_rain = 0
    max_rain = 100

    # Creating an instance of the RainSensorSimulator with coordinates
    simulator = RainSensorSensorSimulator(
        "rain_sensor1", random_obj, datetime_obj, coordinates)

    # Running the simulation 1000 times with different timestamps
    for i in range(24*60):
        # Creating a timestamp for the simulation
        simulated_datetime = datetime(
            2024, 3, 18, 0, 0, 0) + timedelta(minutes=i*5)

        # Mocking datetime.now() to return the simulated_datetime
        with patch.object(simulator, '_datetime_obj') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime
            json_data = simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Extracting the rain intensity value
            intensity = float(parsed_json['readings'][0]['value'])
            # Assert that the rain intensity is within the specified range
            print(intensity)
            assert min_rain <= intensity <= max_rain
    assert False
