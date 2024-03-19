import json
from datetime import datetime, timedelta
from unittest.mock import patch
from src.simulator.reservoir_sensor_simulator import ReservoirSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random


def test_reservoir_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining a specific datetime for the simulation
    # Spring: March 18, 2024 at 17:00:00
    spring_datetime = datetime(2024, 3, 18, 17, 0, 0, 447663)

    # Summer: June 18, 2024 at 17:00:00
    summer_datetime = datetime(2024, 6, 18, 17, 0, 0, 447663)

    # Autumn: September 18, 2024 at 17:00:00
    autumn_datetime = datetime(2024, 9, 18, 17, 0, 0, 447663)

    # Winter: December 18, 2024 at 17:00:00
    winter_datetime = datetime(2024, 12, 18, 17, 0, 0, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', side_effect=[
        80, 0, 0.1, 0.1,
        75, 0, 0.1, 0.1,
        85, 0, 0.1, 0.1,
        90, 0, 0.1, 0.1,]):
        
        with patch.object(Random, 'randint', return_value=0):
            random_obj = Random(123)

            # Mocking datetime object to return the specific datetime
            with patch('datetime.datetime') as mocked_datetime:
                
                # Spring simulation
                mocked_datetime.now.return_value = spring_datetime
                sensor_simulator = ReservoirSensorSimulator("reservoir1", random_obj, mocked_datetime,
                                                                    coordinates)
                # Running the simulate method to get the JSON data
                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)
                # Define the expected JSON structure
                expected_json = {
                    "type": "reservoir",
                    "timestamp": "2024-03-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 80.18}],
                    "name": "reservoir1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }
                # Assert that the parsed JSON matches the expected JSON
                assert parsed_json == expected_json
                
                # Summer simulation
                mocked_datetime.now.return_value = summer_datetime
                sensor_simulator = ReservoirSensorSimulator("reservoir1", random_obj, mocked_datetime,
                                                                    coordinates)
                
                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)

                expected_json = {
                    "type": "reservoir",
                    "timestamp": "2024-06-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 75.20}],
                    "name": "reservoir1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }

                assert parsed_json == expected_json
                
                # Fall simulation
                mocked_datetime.now.return_value = autumn_datetime
                sensor_simulator = ReservoirSensorSimulator("reservoir1", random_obj, mocked_datetime,
                                                                    coordinates)

                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)

                expected_json = {
                    "type": "reservoir",
                    "timestamp": "2024-09-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 85.15}],
                    "name": "reservoir1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }

                assert parsed_json == expected_json
                
                # Winter simulation
                mocked_datetime.now.return_value = winter_datetime
                sensor_simulator = ReservoirSensorSimulator("reservoir1", random_obj, mocked_datetime,
                                                                    coordinates)

                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)

                expected_json = {
                    "type": "reservoir",
                    "timestamp": "2024-12-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 90.14}],
                    "name": "reservoir1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }

                assert parsed_json == expected_json


def test_reservoir_sensor_simulation_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Defining the range for reservoir level
    min_level = 0
    max_level = 100
    
    # Defining specific datetimes for each season
    # Spring: March 18, 2024
    spring_datetime = datetime(2024, 3, 18)

    # Summer: June 18, 2024
    summer_datetime = datetime(2024, 6, 18)

    # Autumn: September 18, 2024
    autumn_datetime = datetime(2024, 9, 18)

    # Winter: December 18, 2024
    winter_datetime = datetime(2024, 12, 18)
    
    # List of seasonal datetimes
    seasonal_datetimes = [spring_datetime, summer_datetime, autumn_datetime, winter_datetime]

    # Running the simulation for each season
    for season_datetime in seasonal_datetimes:
        with patch('datetime.datetime') as mocked_datetime:

            for minute in range(24 * 60):
                # Set the current minute of the day
                mocked_datetime.now.return_value = season_datetime + timedelta(minutes=minute)

                sensor_simulator = ReservoirSensorSimulator("reservoir1", random_obj, mocked_datetime,
                                                                    coordinates)

                # Running the simulate method to get the JSON data
                json_data = sensor_simulator.simulate()

                # Parsing the JSON data
                parsed_json = json.loads(json_data)

                # Extracting the temperature value
                level = parsed_json['readings'][0]['value']

                # Assert that the temperature is within the specified range
                assert min_level <= level <= max_level