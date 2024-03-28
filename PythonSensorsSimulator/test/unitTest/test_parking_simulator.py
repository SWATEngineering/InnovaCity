import json
from datetime import datetime, timedelta
from unittest.mock import patch
from src.simulator.parking_sensor_simulator import ParkingSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random


def test_parking_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    simulated_datetime = datetime(2024, 3, 18, 10, 19, 9, 447663)

    # Mocking random object
    with patch.object(Random, 'normalvariate', return_value=0):
        random_obj = Random()

        # Mocking datetime object to return the specific datetime
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            sensor_simulator = ParkingSensorSimulator("parking1", random_obj, mocked_datetime,
                                                      coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Define the expected JSON structure
            expected_json = {
                "type": "parking",
                "timestamp": "2024-03-18 10:19:09.447663",
                "readings": [{"type": "Number", "value": 49}, {"type": "Number", "value": 100}],
                "name": "parking1",
                "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
            }

            # Assert that the parsed JSON matches the expected JSON
            assert parsed_json == expected_json


def test_parking_sensor_simulation_peak():
    coordinates = Coordinates(45.398214, 11.851271)
    simulated_datetime = datetime(2024, 3, 18, 12, 0, 0, 0)

    # Mocking random object
    with patch.object(Random, 'normalvariate', return_value=0):
        random_obj = Random()

        # Mocking datetime object to return the specific datetime
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            sensor_simulator = ParkingSensorSimulator("parking2", random_obj, mocked_datetime,
                                                      coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Define the expected JSON structure
            expected_json = {
                "type": "parking",
                "timestamp": "2024-03-18 12:00:00",
                "readings": [{"type": "Number", "value": 100}, {"type": "Number", "value": 100}],
                "name": "parking2",
                "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
            }

            # Assert that the parsed JSON matches the expected JSON
            assert parsed_json == expected_json

def test_parking_sensor_simulation_midnight():
    coordinates = Coordinates(45.398214, 11.851271)
    simulated_datetime = datetime(2024, 3, 18, 0, 0, 0, 0)

    # Mocking random object
    with patch.object(Random, 'normalvariate', return_value=0):
        random_obj = Random()

        # Mocking datetime object to return the specific datetime
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            sensor_simulator = ParkingSensorSimulator("parking1", random_obj, mocked_datetime,
                                                      coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Define the expected JSON structure
            expected_value = 0

            assert parsed_json["readings"][0]["value"] == expected_value
