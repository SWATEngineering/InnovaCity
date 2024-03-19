import json
from datetime import datetime, timedelta
from unittest.mock import patch
from src.simulator.wind_sensor_simulator import WindSensorSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random


def test_wind_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    simulated_datetime = datetime(2024, 3, 18, 10, 19, 9, 447663)

    # Mocking random object
    with patch.object(Random, 'random', return_value=0):
        random_obj = Random()

        # Mocking datetime object to return the specific datetime
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            # Creating an instance of the WindSensorSensorSimulator with coordinates
            sensor_simulator = WindSensorSensorSimulator("wind1", random_obj, mocked_datetime, coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Define the expected JSON structure
            expected_json = {
                "type": "wind",
                "timestamp": "2024-03-18 10:19:09.447663",
                "readings": [
                    {"type": "km/h", "value": "2.00"},
                    {"type": "direction", "value": 358}
                ],
                "name": "wind1",
                "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
            }

            # Assert that the parsed JSON matches the expected JSON
            assert parsed_json == expected_json

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Define the expected JSON structure
            expected_json = {
                "type": "wind",
                "timestamp": "2024-03-18 10:19:09.447663",
                "readings": [
                    {"type": "km/h", "value": "2.00"},
                    {"type": "direction", "value": 356}
                ],
                "name": "wind1",
                "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
            }

            # Assert that the parsed JSON matches the expected JSON
            assert parsed_json == expected_json


def test_wind_sensor_simulation_speed_direction_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Defining the range for wind speed
    min_speed = 1
    max_speed = 9

    # Defining the range for wind direction
    min_direction = 0
    max_direction = 360

    # Running the simulation 1000 times with different timestamps
    for i in range(24 * 60):
        # Creating a timestamp for the simulation
        simulated_datetime = datetime(2024, 3, 18, 0, 0, 0) + timedelta(minutes=i)
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            # Creating an instance of the WindSensorSensorSimulator with coordinates
            sensor_simulator = WindSensorSensorSimulator("wind1", random_obj, mocked_datetime, coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Extracting the wind speed value
            speed = float(parsed_json['readings'][0]['value'])

            # Extracting the wind speed value
            direction = float(parsed_json['readings'][1]['value'])

            # Assert that the wind speed is within the specified range
            assert min_speed <= speed <= max_speed
            assert min_direction <= direction <= max_direction
