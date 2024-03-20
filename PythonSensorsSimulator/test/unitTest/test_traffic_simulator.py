import json
from datetime import datetime, timedelta
from unittest.mock import patch
from src.simulator.traffic_sensor_simulator import TrafficSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random


def test_traffic_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    simulated_datetime = datetime(2024, 3, 18, 10, 19, 9, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', return_value=0):
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking datetime object to return the specific datetime
            with patch('datetime.datetime') as mocked_datetime:
                mocked_datetime.now.return_value = simulated_datetime

                # Creating an instance of the TrafficSensorSimulator with coordinates
                sensor_simulator = TrafficSensorSimulator("traffic1", random_obj, mocked_datetime, coordinates)

                # Running the simulate method to get the JSON data
                json_data = sensor_simulator.simulate()

                # Parsing the JSON data
                parsed_json = json.loads(json_data)

                # Define the expected JSON structure
                expected_json = {
                    "type": "traffic",
                    "timestamp": "2024-03-18 10:19:09.447663",
                    "readings": [{"type": "Number", "value": 0}, {"type": "Level", "value": "LOW"},
                                 {"type": "Minutes", "value": 5.0}],
                    "name": "traffic1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }

                # Assert that the parsed JSON matches the expected JSON
                assert parsed_json == expected_json

def test_traffic_sensor_simulation_level():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Defining possible traffic levels
    traffic_levels = ["LOW", "MEDIUM", "HIGH", "BLOCKED"]

    # Running the simulation 1000 times with different timestamps
    for i in range(24*60):
        # Creating a timestamp for the simulation
        simulated_datetime = datetime(2024, 3, 18, 0, 0, 0) + timedelta(minutes=i)
        with patch('datetime.datetime') as mocked_datetime:
            mocked_datetime.now.return_value = simulated_datetime

            # Creating an instance of the TrafficSensorSimulator with coordinates
            sensor_simulator = TrafficSensorSimulator("traffic1", random_obj, mocked_datetime, coordinates)

            # Running the simulate method to get the JSON data
            json_data = sensor_simulator.simulate()

            # Parsing the JSON data
            parsed_json = json.loads(json_data)

            # Extracting the Traffic value
            Level = parsed_json['readings'][1]['value']

            # Assert that the traffic level in the possible cases
            assert Level in traffic_levels

def test_traffic_sensor_update_traffic_level():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Creating an instance of the TrafficSensorSimulator with coordinates
    sensor_simulator = TrafficSensorSimulator("traffic1", random_obj, datetime, coordinates)

    # Testing when __num_cars <= LOW_THRESHOLD
    sensor_simulator._TrafficSensorSimulator__num_cars = TrafficSensorSimulator._TrafficSensorSimulator__LOW_THRESHOLD - 1
    sensor_simulator._update_traffic_level()
    assert sensor_simulator._TrafficSensorSimulator__traffic_level == "LOW"

    # Testing when LOW_THRESHOLD < __num_cars <= MEDIUM_THRESHOLD
    sensor_simulator._TrafficSensorSimulator__num_cars = TrafficSensorSimulator._TrafficSensorSimulator__MEDIUM_THRESHOLD
    sensor_simulator._update_traffic_level()
    assert sensor_simulator._TrafficSensorSimulator__traffic_level == "MEDIUM"

    # Testing when MEDIUM_THRESHOLD < __num_cars <= HIGH_THRESHOLD
    sensor_simulator._TrafficSensorSimulator__num_cars = TrafficSensorSimulator._TrafficSensorSimulator__HIGH_THRESHOLD
    sensor_simulator._update_traffic_level()
    assert sensor_simulator._TrafficSensorSimulator__traffic_level == "HIGH"

    # Testing when __num_cars > HIGH_THRESHOLD
    sensor_simulator._TrafficSensorSimulator__num_cars = TrafficSensorSimulator._TrafficSensorSimulator__HIGH_THRESHOLD + 1
    sensor_simulator._update_traffic_level()
    assert sensor_simulator._TrafficSensorSimulator__traffic_level == "BLOCKED"