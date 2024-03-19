import json
from datetime import datetime,timedelta
from unittest.mock import patch
from src.simulator.humidity_sensor_simulator import HumiditySensorSensorSimulator
from src.utils.coordinates import Coordinates
from random import Random

def test_humidity_sensor_simulation():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Defining specific datetimes for the simulations representing each season
    # Spring: March 18, 2024 at 17:00:00
    spring_datetime = datetime(2024, 3, 18, 17, 0, 0, 447663)

    # Summer: June 18, 2024 at 17:00:00
    summer_datetime = datetime(2024, 6, 18, 17, 0, 0, 447663)

    # Autumn: September 18, 2024 at 17:00:00
    autumn_datetime = datetime(2024, 9, 18, 17, 0, 0, 447663)

    # Winter: December 18, 2024 at 17:00:00
    winter_datetime = datetime(2024, 12, 18, 17, 0, 0, 447663)

    # Mocking random object
    with patch.object(Random, 'uniform', return_value=0):
        with patch.object(Random, 'random', return_value=0):
            random_obj = Random()

            # Mocking datetime object to return specific datetimes for each season
            with patch('datetime.datetime') as mocked_datetime:
                # Spring simulation
                mocked_datetime.now.return_value = spring_datetime
                sensor_simulator = HumiditySensorSensorSimulator("humidity1", random_obj, mocked_datetime,
                                                                    coordinates)
                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)
                expected_json = {
                    "type": "humidity",
                    "timestamp": "2024-03-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 55.23}],
                    "name": "humidity1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }
                assert parsed_json == expected_json

                # Summer simulation
                mocked_datetime.now.return_value = summer_datetime
                sensor_simulator = HumiditySensorSensorSimulator("humidity1", random_obj, mocked_datetime,
                                                                    coordinates)
                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)
                # Define the expected JSON structure for summer
                expected_json = {
                    "type": "humidity",
                    "timestamp": "2024-06-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 60.98}],  # Fill in the expected value for summer
                    "name": "humidity1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }
                assert parsed_json == expected_json

                # Autumn simulation
                mocked_datetime.now.return_value = autumn_datetime
                sensor_simulator = HumiditySensorSensorSimulator("humidity1", random_obj, mocked_datetime,
                                                                    coordinates)
                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)
                # Define the expected JSON structure for autumn
                expected_json = {
                    "type": "humidity",
                    "timestamp": "2024-09-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 53.36}],  # Fill in the expected value for autumn
                    "name": "humidity1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }
                assert parsed_json == expected_json

                # Winter simulation
                mocked_datetime.now.return_value = winter_datetime
                sensor_simulator = HumiditySensorSensorSimulator("humidity1", random_obj, mocked_datetime,
                                                                    coordinates)
                json_data = sensor_simulator.simulate()
                parsed_json = json.loads(json_data)
                # Define the expected JSON structure for winter
                expected_json = {
                    "type": "humidity",
                    "timestamp": "2024-12-18 17:00:00.447663",
                    "readings": [{"type": "%", "value": 44.33}],  # Fill in the expected value for winter
                    "name": "humidity1",
                    "location": {"type": "Point", "coordinates": [45.398214, 11.851271]}
                }
                assert parsed_json == expected_json
                
def test_humidity_sensor_simulation_seasons_range():
    # Creating an instance of Coordinates
    coordinates = Coordinates(45.398214, 11.851271)

    # Mocking random object
    random_obj = Random()

    # Defining the range for humidity
    min_humidity = 30
    max_humidity = 100

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
            # Cycling through the entire day (24 hours * 60 minutes = 1440 minutes) of each season
            for minute in range(24 * 60):
                # Set the current minute of the day
                mocked_datetime.now.return_value = season_datetime + timedelta(minutes=minute)

                # Creating an instance of the HumiditySensorSensorSimulator with coordinates
                sensor_simulator = HumiditySensorSensorSimulator("humidity1", random_obj, mocked_datetime,
                                                                  coordinates)

                # Running the simulate method to get the JSON data
                json_data = sensor_simulator.simulate()

                # Parsing the JSON data
                parsed_json = json.loads(json_data)

                # Extracting the humidity value
                humidity = parsed_json['readings'][0]['value']

                # Assert that the humidity is within the specified range
                assert min_humidity <= humidity <= max_humidity

